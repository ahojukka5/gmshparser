# Performance benchmarks

The repository includes a reproducible benchmark runner for comparing parser
implementations before and after architectural changes. It generates equivalent
quadrilateral grids in ASCII MSH 2.2 and 4.1 format, so benchmark inputs do not
need to be stored in Git or downloaded from external sources.

## Measured phases

The runner measures four public data paths independently:

| Phase | Work measured | Models retained before the phase |
| --- | --- | --- |
| `legacy_parse` | `gmshparser.parse(path)` | none |
| `legacy_to_modern` | `Mesh.from_legacy(legacy)` | parsed compatibility model |
| `read` | complete `gmshparser.read(path)` | none |
| `numpy` | `gmshparser.numpy.to_numpy(modern)` | parsed modern model |

This separation shows whether time and memory are spent reading text, building
the compatibility model, converting to the immutable model, or allocating array
data.

## Running locally

Install only the benchmark dependencies and run the default matrix:

```bash
uv sync --no-default-groups --group benchmark
uv run --no-sync python -m benchmarks.run
```

The default run uses MSH 2.2 and 4.1 grids with `32²`, `100²`, and `224²`
elements, three measured subprocesses, and one warm-up subprocess for every
case. Override any dimension explicitly:

```bash
uv run --no-sync python -m benchmarks.run \
  --formats 2.2,4.1 \
  --sizes 32,100,316 \
  --phases legacy_parse,legacy_to_modern,read,numpy \
  --repeats 5 \
  --warmups 1
```

The command writes machine-readable `benchmark-results.json` and a rendered
`benchmark-summary.md`. Use `--workdir PATH` to retain the generated meshes.

## Memory interpretation

Every measured sample runs in a fresh Python subprocess.

- **Python peak** is the allocation high-water mark during the measured phase
  reported by `tracemalloc`.
- **Peak RSS** is the operating system's whole-process high-water mark.
- `legacy_to_modern` RSS includes the compatibility model that must remain alive
  during conversion.
- `numpy` RSS includes the modern model that remains alive while arrays are
  allocated.

Peak RSS is therefore the more useful estimate for application capacity. Python
peak is useful for locating which phase creates Python-managed objects.

## GitHub Actions

The **Parser benchmarks** workflow runs the default matrix on benchmark-related
pull requests and uploads both reports as an artifact. It can also be launched
manually with custom sizes, repetitions, and warm-ups. The workflow verifies
that benchmarks remain executable but does not compare timings against a fixed
threshold.

## Comparison rules

Benchmark values are not portable between unrelated machines. Compare two runs
only when all of these remain equivalent:

- Python and NumPy versions
- operating system and runner or machine class
- generated formats and grid sizes
- phases, repetitions, and warm-up count
- repository build and dependency configuration

Use median elapsed time for comparisons. Treat small differences on shared CI
runners as noise and look for consistent changes across multiple sizes.

## Current reference baseline

The first GitHub-hosted reference baseline will be recorded here from the
benchmark workflow introduced with this page.
