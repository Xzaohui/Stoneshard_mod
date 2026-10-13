# Purple Crystal HD-2D - Design Spec

## I. Project Information

Full inventory: 745 initial view slots. Active batch: N1 three rooms and separate architectural/story assets. Status: production in progress.

## II. Canvas Specification

26×26 game cells; three 1040×780 local scenes. Building export 312×260; prop sheet 624×416. Camera: orthographic oblique over square grid.

## III. Color Palette

DEN-N1-128; all HEX values in spec_lock.md and palettes/den_n1_128.json. Existing DEN concept image supplies the material colors. Revised after visual QA found coarse neutral ramps in the first 64-color sampling.

## IV. Art Style Definition

Crisp textured medieval HD-2D, worn timber, limestone and dark tidal water; restrained top-left light. Independent art depth passes; no crystal effects in this chapter.

## V. Asset List

Production geometry: native_layouts.json. Full requirements: inventory.json. Generation records: generation-log.json. Unfinished requirements remain open.

## VI. Animation Specification

Single static frame per export. Existing in-engine NPC and candle behavior is not baked into art.

## VII. Technical Constraints

Native source geometry is authoritative. Preserve door/arrival/story coordinates. Validate dimensions, alpha, palette, source hashes, connectivity, and actual visual fit independently.

## VIII. Platform Export Notes

GameMaker-compatible RGBA PNG with relative paths, origin and draw-layer metadata. Exports are not a modified data.win or an accepted in-game test.
