# Framework status and entry points

## Implemented

- Shared graph conversion, fixed teaching input and CSV formatting.
- Matrix/array Dijkstra and indexed binary heap/list Dijkstra.
- Connected random generator with exact n/m and reproducible seeds.
- Shared test-only Bellman-Ford reference and independent integration checks.
- Random-input CLI and check/timing/count pipeline.
- Full C++ tests and standard-library Python CLI validation.

## Pending

Python batch experiment execution, aggregation and plotting logic remain TODOs in experiments/scripts/. Their --help parsers exist but actual processing still exits PENDING. This is separate from the now-working C++ measurement entry point.

## Commands

```bash
make -j2 all test
./build/dijkstra_benchmark --help
./build/dijkstra_benchmark --demo matrix
./build/dijkstra_benchmark --demo heap
./build/dijkstra_benchmark --n 20 --m 80 --seed 2001 --mode check
./build/dijkstra_benchmark --n 20 --m 80 --seed 2001 --mode count
./build/dijkstra_benchmark --n 20 --m 80 --seed 2001 --mode timing --repeats 3
```

All source functions return actual results; no fabricated placeholder data are used. Full make test checks algorithms, generator, reference integration and CLI. See [running guide](running-guide.md) for flags, timing boundaries, CSV schemas and pilot records.

## Files and ownership

| Files | Purpose |
| --- | --- |
| include/types.hpp, graph.hpp, generation.hpp | Shared types and input contract |
| include/dijkstra.hpp, min_heap.hpp | Algorithm/queue interfaces |
| include/benchmark.hpp, output.hpp | Measurement configuration and serialization |
| src/graph.cpp, generation.cpp | Shared graph construction |
| src/dijkstra_matrix.cpp | Matrix/array algorithm |
| src/min_heap.cpp, dijkstra_heap.cpp | Indexed-heap algorithm |
| src/main.cpp, benchmark.cpp, output.cpp | CLI, verification, measurement, output |
| tests/reference_bellman_ford.hpp, test_dijkstra.cpp | Independent integration validation |
| tests/test_cli.py | Public CLI and CSV/error checks |

Member A/B implementation responsibilities and original handoffs remain in [team roles](team-roles.md); Member C owns generation/measurement/automation and coordinates analysis. Both algorithms use shared DijkstraResult and OperationStats. Source/unreachable parents are empty; absence is INF; equal priorities use vertex ID. Keep clocks/output/generation outside algorithm functions.
