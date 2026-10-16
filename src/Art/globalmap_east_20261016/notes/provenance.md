# globalmap_east_20261016 provenance

- Spec: `work/code` @ `831a188f` · `docs/roadmap/大地图扩充方案-20261016.md` §6
- Date: 2026-10-16 (Asia/Shanghai)

## layout/
- `east_layout_cells.txt` — exact cell table from §4 ASCII (x36–49, y22–40)
- `east_layout.png` / `east_layout_paper.png` — 728×988, 52 px/cell
  - art_source: code (Pillow), palette sampled from official wiki `Global_Map.png`
  - style target: Stoneshard global map ink + light wash; paper = sepia/parchment remapping
  - purpose: planning sketch only (定稿用，不进游戏)

## icons/
- `s_eao_gl_greybank.png` + `_paper.png` — 灰堤外院 · Codex `image_gen` then key/fit to 52×52
- `s_eao_gl_ferry.png` + `_paper.png` — 河口旧渡口 · same pipeline · 52×55~56
- Quarry icon: reuse vanilla `s_gabadonedquarry_steppe` (not shipped here)

## not produced
- Decals / terrain tiles (reuse originals)
- sites/quarry scene shadow fixes (deferred)
