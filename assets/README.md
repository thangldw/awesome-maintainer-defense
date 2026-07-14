# Release visuals

- `social-preview.svg` is the editable 1280×640 source; `social-preview.png` is the solid-background GitHub upload and stays below GitHub's 1 MB limit.
- `demo.gif` is 1280×720, eight frames, and 35.5 seconds. `scripts/render_demo.mjs` runs the standalone CLI against a temporary repository before rendering its captured output.
- Both render scripts require Node.js and `sharp`; the release CLI itself has no third-party dependency.

The visual hierarchy uses one message, one focal object, limited colors, strong spacing, and left-to-right scanning. Decision diagrams elsewhere in the repository follow the separate Miro-inspired conventions in [`docs/VISUAL_STYLE.md`](../docs/VISUAL_STYLE.md).
