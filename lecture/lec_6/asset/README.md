# Lecture 6 diagram assets

`model-context-protocol.svg` is the editable source for the MCP architecture
on slide 9. `model-context-protocol.pdf` is its vector export used by pdfLaTeX.
The SVG keeps editable text labels and shapes rather than embedding a bitmap.

The layout adapts IBM's [What is Model Context Protocol?](https://www.ibm.com/think/topics/model-context-protocol).
The original `model-context-protocol.png` is retained for provenance. The
adaptation replaces the old HTTP+SSE transport labels with Streamable HTTP,
following the official [MCP Transports specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports).
Local stdio connections are retained. Slide source credit names both sources.

After editing the SVG, export it as PDF in an SVG editor, or use librsvg's CLI
from the repository root:

```bash
rsvg-convert --format=pdf \
  --output=lecture/lec_6/asset/model-context-protocol.pdf \
  lecture/lec_6/asset/model-context-protocol.svg
```

The conversion utility is an optional system tool; normal slide builds use the
committed PDF and require no new Python dependency. Rebuild `lecture_6.pdf`
with the command in the lecture README after updating the vector export.

`bounded-agent-loop.svg` is original course artwork used on the course website.
