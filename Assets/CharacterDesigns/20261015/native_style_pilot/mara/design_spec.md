# Design Specification

## Overview
Two Mara-only style pilot assets. Approval is for a first production pass and subsequent review, not in-game integration.

## Visual Direction
Use the supplied v4 direction, large locks and large hard-edged planes, with structurally resolved nose and cheeks. The character remains a mature, guarded ropeworker.

## Asset Requirements
- Dialogue portrait: 74×100.
- Map idle: 35×44, independently generated.

## Quality Gates
Measure real source pixels; preserve exact raw outputs; no inferred source dimensions from collage labels. Export target-size candidates and inspect both 1x and nearest-neighbor integer enlargement. Retain failed candidates.

## Constraints
No runtime integration. Vendor pixel tool scripts are absent. Independent Pillow mechanical QA is not a replacement claim for missing official validators.
