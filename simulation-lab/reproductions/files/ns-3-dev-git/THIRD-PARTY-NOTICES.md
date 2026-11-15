# Third-party sources

The build harness downloads sources; this small bundle contains original orchestration and generated results.

- ns-3 / Unison: https://github.com/NASA-NJU/UNISON-for-ns-3 at 7b3274167615c55ae8d69f7edee4e2dc2d81f706; GPL-2.0. Retain LICENSE and individual notices.
- SimGrid coordinator-worker benchmark: https://github.com/simgrid/coordinator_worker_flashback at b09453d19541b7186703f4d651c1bba790461e44. Both C/C++ model files retain SimGrid-team copyright and GNU LGPL notices referring to their package license.
- SimGrid3.10 and3.36 source: LGPL-2.1 core, with component-specific notices in COPYING and LICENSE-LGPL-2.1. The path patch preserves source notices; the build-system workaround is taken from the authors’ Dockerfile.
- Boost: retain the Boost Software License and exact dependency provenance for the prefix selected at build.
- Papers are cited and linked, not redistributed in the public bundle. Only numerical reference entries necessary for the comparison are transcribed with attribution.

Original OSRI harnesses are covered by the hub’s original-code license; original guides/results/figures follow the hub’s documentation/data licensing. Third-party source and assets retain their own terms.
