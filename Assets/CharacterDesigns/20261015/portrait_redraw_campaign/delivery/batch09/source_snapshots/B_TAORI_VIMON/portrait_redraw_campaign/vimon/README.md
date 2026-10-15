# vimon portrait redraw candidate

Built-in image_gen substantive redraw, then explicitly NON-NATIVE nearest-neighbor 74×100 derivative with ≤32 temporary visible colors and binary alpha. The full raw image and complete tool result are preserved. No hand pixel edits. No character-card, historical-art, runtime or code replacement. No commits or pushes.

Current stage: portrait_v2 selected by author after the single necessary correction; independent final QA: candidate_with_notes. Both v1 and v2 are preserved. Revision budget exhausted.

- Source and identity lock: spec_lock.md; sources/source_manifest.json
- Exact generation parameters: prompts/portrait_v1.json and portrait_v2.json
- Full tool return and unaltered PNG: tool_returns/portrait_v1.json and portrait_v2.json; corresponding raw/*.png
- Target and 1x / 8x previews: candidates/ and previews/
- Deterministic derivation: python derive_portrait.py portrait_v2
- Technical metrics and reviews: qa/
- Integrity inventory: manifest.json and SHA256SUMS.txt

The color ceiling is temporary, not proof of a hand-designed native palette. Neither image nor file validation establishes user approval or in-game verification.

Freeze: independent reviewer audit_campaign_ninth_batch confirmed candidate_with_notes on 2026-10-15. Selected image unchanged after confirmation. All inputs, raw returns, derived PNGs, previews and manifests verified; no native pixel or runtime approval is claimed.
