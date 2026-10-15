# 阿霖 portrait redraw candidate

Selected: candidates/portrait_v2_inset_74x100_candidate.png
Status: independently accepted redraw candidate with limitations; selected SHA frozen.

Two successful built-in image_gen outputs: initial draft plus one necessary revision. Current identity card, mother image and mother QA, three scene-source documents and four core style references have exact source snapshots and SHA records. Full prompts, parameters and tool returns are retained. One six-reference payload was rejected before generation; its unchanged error record is saved, and the actual revision used five references.

Method: 74×100 technical derivative from entire raw canvas. Isotropic nearest-neighbor fit within 72×98, centered on transparent 74×100; alpha threshold 128; MAXCOVERAGE <=32 temporary visible colors, no dithering. No crop, no drawing facial features in scripts. The imagegen redraw and this technical derivative are not a native hand-authored pixel final. No runtime integration or game validation.

Reproduce selected derivative: python derive_portrait.py portrait_v2 inset
Rebuild manifests: python finalize_manifest.py portrait_v2_inset accepted_redraw_candidate_with_notes

Previews include exact 1x, nearest-neighbor 8x and 1x/4x dark-gray-light composites. Sources were reread and hash-checked unchanged. Old assets, cards, code and global campaign files are preserved. No commit or push.

Known limitations:
- Some parallel broad hair subdivisions remain.
- Muted light sclera and inner-brow worry remain more visible than ideal minimal-eye design.
- The full export shows olive merging in some hair/beard colors; selected inset reduces this, though some dark-color merging remains. Unquantized raw is retained.

Independent reviewer: /root/audit_campaign_twentyfirst_batch. Both v2 raw images already preserve the whole silhouette; the inset is technical containment, not repair of a cropped source.
