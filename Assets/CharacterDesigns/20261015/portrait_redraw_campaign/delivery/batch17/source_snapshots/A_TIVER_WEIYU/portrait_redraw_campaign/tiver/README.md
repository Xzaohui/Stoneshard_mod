# tiver dialogue portrait candidate

Selected: `candidates/portrait_v2_74x100_candidate.png`.

Imagegen made a substantial new portrait. Raw image and exact tool return are archived. This 74×100 image is an explicitly technical nearest-neighbor and no-dither palette derivative, not native 74×100 pixel authorship and not game-ready/runtime-approved.

The exporter uses one isotropic scalar, inverse mapping destination pixel centers with nearest-neighbor sampling, transparent padding if needed, alpha threshold 128, and a maximum of 32 visible RGB colors through MAXCOVERAGE palette selection with no dithering. When an explicitly named safety variant is selected, it uses a 72×98 fit region centered in the transparent 74×100 target; otherwise the full 74×100 fit region is used. This only supplies an export margin and does not redraw or crop the image. It performs no facial drawing, geometry repair, paintover, crop, or smoothing. The 32-color ceiling is a temporary working constraint, not a claim that all project art must use exactly 32 colors.

`previews/portrait_v2_1x_8x.png` contains 1x dark/gray/light composites and an integer 8x nearest-neighbor preview. Four core references are archived separately as style-only anchors.

Reproduce from the repository root:

`python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/tiver/derive_portrait.py Assets/CharacterDesigns/20261015/portrait_redraw_campaign/tiver portrait_v2 `

Full prompts/parameters: `prompts/`. Full responses: `tool_returns/`. Raw outputs: `raw/`. Current cards, old identity, QA, manifests, story constraints and SHA registry: `sources/`. Identity, technical checks, deterministic rerun and preservation checks: `qa/`.

Two calls maximum: first draft and one targeted correction. Previous assets, cards, implementation code and global indexes remain unchanged. No commit/push or runtime integration was performed.
