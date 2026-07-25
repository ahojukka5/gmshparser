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
peak is useful for locating which phase creates Python-managed objects. Compare
RSS values for the same phase across revisions; retained prerequisite models and
tracing overhead differ between phases.

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

The first reference was produced by GitHub Actions run `30133127529` on
2026-07-24 using Python 3.12.3, NumPy 2.5.1, Ubuntu/Azure Linux, two measured
subprocesses, and one warm-up subprocess. The complete median dataset is stored
in:

```text
benchmarks/baselines/2026-07-24-github-ubuntu-python312.json
```

The largest generated case contained 50,625 nodes and 50,176 quadrilateral
elements:

| MSH | Phase | Median ms | Python peak MiB | Peak RSS MiB |
| --- | --- | ---: | ---: | ---: |
| 2.2 | `legacy_parse` | 2,975.04 | 40.2 | 144.7 |
| 2.2 | `legacy_to_modern` | 1,606.45 | 33.4 | 109.4 |
| 2.2 | `read` | 4,704.81 | 69.7 | 187.7 |
| 2.2 | `numpy` | 740.78 | 14.3 | 116.2 |
| 4.1 | `legacy_parse` | 1,728.14 | 31.5 | 128.6 |
| 4.1 | `legacy_to_modern` | 1,474.98 | 25.6 | 93.9 |
| 4.1 | `read` | 3,289.23 | 57.1 | 167.8 |
| 4.1 | `numpy` | 741.76 | 14.3 | 107.0 |

### Baseline interpretation

- Complete `read()` time scales close to linearly across the 1,024, 10,000, and
  50,176 element cases.
- At 50,176 elements, MSH 4.1 completes `read()` about 30% faster than MSH 2.2.
- Legacy-to-modern conversion accounts for about 34% of MSH 2.2 `read()` time
  and 45% of MSH 4.1 `read()` time at the largest size.
- The original complete `read()` path reaches approximately 188 MiB peak RSS for
  MSH 2.2 and 168 MiB for MSH 4.1 at roughly 50,000 elements.

These values define the comparison point for replacing the legacy intermediate
model in the modern `read()` path.

## Direct modern builder result

GitHub Actions run `30135605746` measured the final direct-builder implementation
on the same Python version, runner class, mesh sizes, repetition count, and
warm-up count as the stored reference. At 50,176 elements:

| MSH | Original `read` ms | Direct `read` ms | Time change | Original RSS MiB | Direct RSS MiB | RSS change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2.2 | 4,704.81 | 4,498.60 | -4.4% | 187.7 | 180.1 | -4.0% |
| 4.1 | 3,289.23 | 2,791.24 | -15.1% | 167.8 | 165.7 | -1.3% |

The direct builder removes the complete compatibility object graph and the
separate `Mesh.from_legacy()` pass from `gmshparser.read()`. The compatibility
`gmshparser.parse()` path remains available and continues to build the original
mutable model.

The MSH 2.2 parser also carries per-element physical tags in its raw element
blocks and aggregates entity tags once per entity instead of performing repeated
builder dictionary updates for every element. This was necessary to turn the
initial flat-format regression into a measurable improvement.
