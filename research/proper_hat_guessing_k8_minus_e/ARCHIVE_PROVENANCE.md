# Sealed archive provenance

The three source archives were authenticated before this disclosure was
assembled. Their contents are preserved under the corresponding directories.

| Public directory | Original archive | Size (bytes) | SHA-256 |
|---|---|---:|---|
| `accepted_construction/` | `HGP_K8E_PGL_MATCHING_CLOSURE_20260904_v1.zip` | 767431 | `179c7927cc415e7e3def84f627c0690c3f7b5ab8aeac70d940cd1e6e875825b6` |
| `shared_completion_companion/` | `HGP_K8E_DIAGONAL_SAFE_COMPATIBILITY_20260904_v1.zip` | 1868258 | `22e86756cad1458234d8e51f660d12b83e2164c907ace693ea1508b7ea7bd484` |
| `supporting_gate23/` | `HGP_K8E_GATE23_REPAIRED_20260904_v2.zip` | 191839 | `1ed4e41eba4fec84840edb56eb1d3f7b9e6a945808b88e4e98609088338bd7db` |

Verification before publication reproduced:

```text
accepted construction manifest:             PASS
accepted construction regeneration:         PASS
accepted construction orbit/matching check: PASS
full 138,378,240-colouring check:            PASS

shared-completion family certificate:        PASS
all 136 pilot certificates:                  PASS
four semantic negative controls:             REJECTED as intended

repaired Gate 2/3 manifest and predicates:   PASS
```

The archive SHA-256 values identify the original ZIP byte streams. The checked
in directory trees are authenticated internally by their own manifests; Git
history supplies the public identity of the extracted disclosure.
