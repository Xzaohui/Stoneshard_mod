# 尤恩 portrait redraw candidate

Selected: candidates/portrait_v2_inset_74x100_candidate.png
Status: independently accepted redraw candidate with limitations; selected SHA frozen.

Two successful built-in image_gen outputs: initial draft plus one necessary revision. Current identity card, mother image and mother QA, three scene-source documents and four core style references have exact source snapshots and SHA records. Full prompts, parameters and tool returns are retained. One six-reference payload was rejected before generation; its unchanged error record is saved, and the actual revision used five references.

Method: 74×100 technical derivative from entire raw canvas. Isotropic nearest-neighbor fit within 72×98, centered on transparent 74×100; alpha threshold 128; MAXCOVERAGE <=32 temporary visible colors, no dithering. No crop, no drawing facial features in scripts. The imagegen redraw and this technical derivative are not a native hand-authored pixel final. No runtime integration or game validation.

Reproduce selected derivative: python derive_portrait.py portrait_v2 inset
Rebuild manifests: python finalize_manifest.py portrait_v2_inset accepted_redraw_candidate_with_notes

Previews include exact 1x, nearest-neighbor 8x and 1x/4x dark-gray-light composites. Sources were reread and hash-checked unchanged. Old assets, cards, code and global campaign files are preserved. No commit or push.

Known limitations:
- Forehead wrinkles and a few hair divisions remain more illustrative than ideal native pixel economy.
- Raised inner brows and downturned mouth remain prominent, consistent with historical mother but less varied than an ideal expression library.
- Tiny old pin is reduced to a few subdued pixels in the 74x100 derivative.

Independent reviewer: /root/audit_campaign_twentyfirst_batch. Both v2 raw images already preserve the whole silhouette; the inset is technical containment, not repair of a cropped source.
