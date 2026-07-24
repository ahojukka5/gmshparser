"""Generate representative meshes and benchmark the public read paths."""

from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import gmshparser
from gmshparser.api import Mesh as ModernMesh

try:
    import resource
except ImportError:  # pragma: no cover - unavailable on Windows
    resource = None

PHASES = ("legacy_parse", "legacy_to_modern", "read", "numpy")
FORMATS = ("2.2", "4.1")


def _node_tag(i: int, j: int, width: int) -> int:
    return j * width + i + 1


def _write_msh22(path: Path, cells_per_axis: int) -> tuple[int, int]:
    width = cells_per_axis + 1
    number_of_nodes = width * width
    number_of_elements = cells_per_axis * cells_per_axis

    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("$MeshFormat\n2.2 0 8\n$EndMeshFormat\n")
        stream.write(f"$Nodes\n{number_of_nodes}\n")
        for j in range(width):
            for i in range(width):
                tag = _node_tag(i, j, width)
                stream.write(f"{tag} {float(i)} {float(j)} 0.0\n")
        stream.write("$EndNodes\n")

        stream.write(f"$Elements\n{number_of_elements}\n")
        element_tag = 1
        for j in range(cells_per_axis):
            for i in range(cells_per_axis):
                lower_left = _node_tag(i, j, width)
                lower_right = _node_tag(i + 1, j, width)
                upper_right = _node_tag(i + 1, j + 1, width)
                upper_left = _node_tag(i, j + 1, width)
                stream.write(
                    f"{element_tag} 3 2 1 1 {lower_left} {lower_right} "
                    f"{upper_right} {upper_left}\n"
                )
                element_tag += 1
        stream.write("$EndElements\n")

    return number_of_nodes, number_of_elements


def _write_msh41(path: Path, cells_per_axis: int) -> tuple[int, int]:
    width = cells_per_axis + 1
    number_of_nodes = width * width
    number_of_elements = cells_per_axis * cells_per_axis

    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write("$MeshFormat\n4.1 0 8\n$EndMeshFormat\n")
        stream.write(
            f"$Nodes\n1 {number_of_nodes} 1 {number_of_nodes}\n"
            f"2 1 0 {number_of_nodes}\n"
        )
        for tag in range(1, number_of_nodes + 1):
            stream.write(f"{tag}\n")
        for j in range(width):
            for i in range(width):
                stream.write(f"{float(i)} {float(j)} 0.0\n")
        stream.write("$EndNodes\n")

        stream.write(
            f"$Elements\n1 {number_of_elements} 1 {number_of_elements}\n"
            f"2 1 3 {number_of_elements}\n"
        )
        element_tag = 1
        for j in range(cells_per_axis):
            for i in range(cells_per_axis):
                lower_left = _node_tag(i, j, width)
                lower_right = _node_tag(i + 1, j, width)
                upper_right = _node_tag(i + 1, j + 1, width)
                upper_left = _node_tag(i, j + 1, width)
                stream.write(
                    f"{element_tag} {lower_left} {lower_right} "
                    f"{upper_right} {upper_left}\n"
                )
                element_tag += 1
        stream.write("$EndElements\n")

    return number_of_nodes, number_of_elements


def generate_grid(
    path: Path,
    msh_format: str,
    cells_per_axis: int,
) -> tuple[int, int]:
    """Write a deterministic quadrilateral grid and return node/element counts."""
    if cells_per_axis <= 0:
        raise ValueError("cells_per_axis must be positive")
    if msh_format == "2.2":
        return _write_msh22(path, cells_per_axis)
    if msh_format == "4.1":
        return _write_msh41(path, cells_per_axis)
    raise ValueError(f"Unsupported benchmark MSH format: {msh_format}")


def _maximum_rss_bytes() -> int | None:
    if resource is None:
        return None
    maximum_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return int(maximum_rss)
    return int(maximum_rss * 1024)


def _result_counts(result: object) -> tuple[int, int]:
    if hasattr(result, "get_number_of_nodes"):
        return (
            int(result.get_number_of_nodes()),
            int(result.get_number_of_elements()),
        )
    if hasattr(result, "number_of_nodes"):
        return int(result.number_of_nodes), int(result.number_of_elements)
    if isinstance(result, ModernMesh):
        return len(result.nodes), len(result.elements)
    raise TypeError(f"Cannot determine benchmark result counts for {type(result)!r}")


def _operation(phase: str, mesh_path: Path) -> Callable[[], object]:
    if phase == "legacy_parse":
        return lambda: gmshparser.parse(str(mesh_path))

    if phase == "legacy_to_modern":
        legacy = gmshparser.parse(str(mesh_path))
        return lambda: ModernMesh.from_legacy(legacy)

    if phase == "read":
        return lambda: gmshparser.read(mesh_path)

    if phase == "numpy":
        import gmshparser.numpy as gnp

        modern = gmshparser.read(mesh_path)
        return lambda: gnp.to_numpy(modern)

    raise ValueError(f"Unknown benchmark phase: {phase}")


def _worker(mesh_path: Path, phase: str) -> dict[str, int | float | None]:
    operation = _operation(phase, mesh_path)
    gc.collect()
    tracemalloc.start()
    started = time.perf_counter_ns()
    result = operation()
    elapsed_ns = time.perf_counter_ns() - started
    _, python_peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    number_of_nodes, number_of_elements = _result_counts(result)

    return {
        "seconds": elapsed_ns / 1_000_000_000,
        "python_peak_bytes": python_peak_bytes,
        "rss_bytes": _maximum_rss_bytes(),
        "number_of_nodes": number_of_nodes,
        "number_of_elements": number_of_elements,
    }


def _run_child(mesh_path: Path, phase: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "benchmarks.run",
            "--worker",
            "--mesh",
            str(mesh_path),
            "--phase",
            phase,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError("Benchmark worker produced no JSON output")
    return json.loads(lines[-1])


def _median(values: Sequence[int | float | None]) -> int | float | None:
    present = [value for value in values if value is not None]
    if not present:
        return None
    return statistics.median(present)


def _summarize_samples(samples: list[dict[str, Any]]) -> dict[str, Any]:
    seconds = [sample["seconds"] for sample in samples]
    python_peaks = [sample["python_peak_bytes"] for sample in samples]
    rss_values = [sample["rss_bytes"] for sample in samples]
    return {
        "median_seconds": _median(seconds),
        "minimum_seconds": min(seconds),
        "maximum_seconds": max(seconds),
        "median_python_peak_bytes": _median(python_peaks),
        "median_rss_bytes": _median(rss_values),
        "samples": samples,
    }


def _format_mebibytes(value: int | float | None) -> str:
    if value is None:
        return "-"
    return f"{value / (1024 * 1024):.1f}"


def _markdown_report(report: dict[str, Any]) -> str:
    environment = report["environment"]
    settings = report["settings"]
    lines = [
        "# gmshparser benchmark results",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Commit: `{environment['commit']}`",
        f"- Python: `{environment['python']}`",
        f"- Platform: `{environment['platform']}`",
        f"- gmshparser: `{environment['gmshparser']}`",
        f"- NumPy: `{environment['numpy']}`",
        f"- Repeats: `{settings['repeats']}` after `{settings['warmups']}` warm-up run(s)",
        "",
        "Each measurement runs in a fresh subprocess. `Python peak` is the memory",
        "allocated during the measured phase according to `tracemalloc`. `Peak RSS`",
        "is the whole process high-water mark, including prerequisite models retained",
        "for `legacy_to_modern` and `numpy`.",
        "",
        "| MSH | Grid | Nodes | Elements | File MiB | Phase | Median ms | Python peak MiB | Peak RSS MiB |",
        "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |",
    ]

    for result in report["results"]:
        lines.append(
            "| "
            f"{result['msh_format']} | "
            f"{result['cells_per_axis']}² | "
            f"{result['number_of_nodes']} | "
            f"{result['number_of_elements']} | "
            f"{result['file_size_bytes'] / (1024 * 1024):.2f} | "
            f"`{result['phase']}` | "
            f"{result['median_seconds'] * 1000:.2f} | "
            f"{_format_mebibytes(result['median_python_peak_bytes'])} | "
            f"{_format_mebibytes(result['median_rss_bytes'])} |"
        )

    lines.extend(
        [
            "",
            "These numbers are a comparison baseline, not a CI performance gate.",
            "Compare results only when the Python version, machine class, benchmark",
            "settings, and generated mesh sizes are equivalent.",
            "",
        ]
    )
    return "\n".join(lines)


def _parse_csv(value: str) -> list[str]:
    values = [item.strip() for item in value.split(",") if item.strip()]
    if not values:
        raise argparse.ArgumentTypeError("Expected at least one comma-separated value")
    return values


def _parent(args: argparse.Namespace) -> int:
    formats = _parse_csv(args.formats)
    phases = _parse_csv(args.phases)
    sizes = [int(value) for value in _parse_csv(args.sizes)]

    unknown_formats = set(formats) - set(FORMATS)
    unknown_phases = set(phases) - set(PHASES)
    if unknown_formats:
        raise ValueError(f"Unsupported formats: {sorted(unknown_formats)}")
    if unknown_phases:
        raise ValueError(f"Unsupported phases: {sorted(unknown_phases)}")
    if any(size <= 0 for size in sizes):
        raise ValueError("All grid sizes must be positive")
    if args.repeats <= 0:
        raise ValueError("repeats must be positive")
    if args.warmups < 0:
        raise ValueError("warmups cannot be negative")

    import numpy as np

    temporary_directory: tempfile.TemporaryDirectory[str] | None = None
    if args.workdir is None:
        temporary_directory = tempfile.TemporaryDirectory(prefix="gmshparser-bench-")
        workdir = Path(temporary_directory.name)
    else:
        workdir = args.workdir
        workdir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    try:
        for msh_format in formats:
            for cells_per_axis in sizes:
                mesh_path = workdir / f"grid-{msh_format}-{cells_per_axis}.msh"
                number_of_nodes, number_of_elements = generate_grid(
                    mesh_path,
                    msh_format,
                    cells_per_axis,
                )
                file_size_bytes = mesh_path.stat().st_size

                for phase in phases:
                    for _ in range(args.warmups):
                        _run_child(mesh_path, phase)
                    samples = [
                        _run_child(mesh_path, phase) for _ in range(args.repeats)
                    ]
                    summary = _summarize_samples(samples)
                    results.append(
                        {
                            "msh_format": msh_format,
                            "cells_per_axis": cells_per_axis,
                            "number_of_nodes": number_of_nodes,
                            "number_of_elements": number_of_elements,
                            "file_size_bytes": file_size_bytes,
                            "phase": phase,
                            **summary,
                        }
                    )
    finally:
        if temporary_directory is not None:
            temporary_directory.cleanup()

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "environment": {
            "commit": os.environ.get("GITHUB_SHA", "unknown"),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmshparser": gmshparser.__version__,
            "numpy": np.__version__,
        },
        "settings": {
            "formats": formats,
            "sizes": sizes,
            "phases": phases,
            "repeats": args.repeats,
            "warmups": args.warmups,
        },
        "results": results,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown = _markdown_report(report)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(markdown, encoding="utf-8")
    print(markdown)
    return 0


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formats", default=",".join(FORMATS))
    parser.add_argument("--sizes", default="32,100,224")
    parser.add_argument("--phases", default=",".join(PHASES))
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--warmups", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("benchmark-results.json"))
    parser.add_argument(
        "--markdown",
        type=Path,
        default=Path("benchmark-summary.md"),
    )
    parser.add_argument("--workdir", type=Path)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--mesh", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--phase", choices=PHASES, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _argument_parser().parse_args(argv)
    if args.worker:
        if args.mesh is None or args.phase is None:
            raise ValueError("Worker mode requires --mesh and --phase")
        print(json.dumps(_worker(args.mesh, args.phase)))
        return 0
    return _parent(args)


if __name__ == "__main__":
    raise SystemExit(main())
