# 瑟拉 Sela portrait candidate

Selected: `candidates/portrait_v1_maxcoverage_74x100_candidate.png` (32 visible colors, binary alpha).

Substantive built-in imagegen redraw based on the exact G identity master and current card. The 74×100 result is an entire-canvas NEAREST + alpha threshold 128 + MAXCOVERAGE quantized derivative, not native pixel authorship. Old assets/cards/code remain unchanged; no commit/push or runtime integration.

Reproduce: `python derive_portrait.py`, then `python export_maxcoverage.py portrait_v1`. Both MEDIANCUT and MAXCOVERAGE variants are retained. Raw tool return, exact prompt, source copies and hashes are included.

Independent QA selected v1 MAXCOVERAGE; minor generous top gap and neck retained rather than risking identity through unnecessary redraw.
