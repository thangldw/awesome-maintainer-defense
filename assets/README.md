# Release visuals

> Generated release assets. Product and documentation contracts remain canonical in the repository root and [`docs/`](../docs/README.md).

- `social-preview.svg` is the editable 1280×640 source; `social-preview.png` is the solid-background GitHub upload and stays below GitHub's 1 MB limit.
- `audit-result.svg` and `audit-result.png` show the real compact output locked by the `pwn-request` corpus regression test. The PNG is suitable for README and release notes.
- `demo.gif` is 1280×720, eight frames, and 35.5 seconds. `scripts/render_demo.mjs` runs the standalone CLI against a temporary repository before rendering its captured output.
- The render scripts require Node.js and `sharp`; the release CLI itself has no third-party dependency. `scripts/render_social_preview.mjs` renders both static PNG files from their SVG sources.

The visual hierarchy uses one message, one focal object, limited colors, strong spacing, and left-to-right scanning. Decision diagrams elsewhere in the repository follow the separate Miro-inspired conventions in [`docs/VISUAL_STYLE.md`](../docs/VISUAL_STYLE.md).
