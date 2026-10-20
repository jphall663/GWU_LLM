- Use the GW LaTeX template for all slide outputs. 
  - All LaTeX slides should include the CC license text on the title slide. 

- Use the provided notation to the extent feasible. 

- All jupyter notebooks should have a header with an MIT license and title, and each cell should have a title; all code complexities should be explained with in-line comments.

- When developing outputs, do not refer explicitly to prompts or instructions. 
 - For example, a title "3. The example MLP, drawn at full size" should be simply "3. The example MLP".
 - For example, do not bold text simply because it was mentioned in an instruction.
 
- Update the root `README.md` for changes to code setup or contents at the lecture level. 
  - Keep `uv` artifacts and instructions up to date in the project `README.md`.
  
- If I ask a conceptual or coding question, please add the response into a `instructor_notes.md` for the corresponding lecture folder.

- Update `index.md` as new class materials become available, following my more established responsible machine learning class here: `https://jphall663.github.io/GWU_rml/`.

- For LaTeX lecture slides, use a consistent citation pattern:
  - Cite academic claims in text with `\parencite{key}` and include a `References` section generated from BibTeX.
  - Give every used BibTeX entry a working `url` field that resolves to the paper, publisher, or official source.
  - Credit external visuals and teaching resources in a small source line on the slide using an author or organization, year, descriptive title, and clickable link.
  - Prefer relevant on-disk materials when they support the topic, but attribute reused visuals to a named creator or organization and a descriptive, linked source. Do not use generic slide attributions such as "local course material."
  - Give each substantive instructional image or diagram a brief, unnumbered description of what it shows; decorative marks, logos, and recurring template graphics do not require descriptions.
  - Use figure numbers only when all substantive visuals in the deck participate in one consistent numbering scheme and the slides refer to those numbers.
  - Center substantive images horizontally and vertically within their slide or column, using vertically centered Beamer columns where appropriate.
  - Keep reference slides typographically plain: suppress decorative bibliography-item icons and omit Roman numerals or other continuation suffixes from repeated `References` frame titles.
  - Set reference-entry text to `\small` or smaller. With `biblatex`, set `\bibfont` explicitly (for example, `\renewcommand*{\bibfont}{\scriptsize}`), because a frame-level size declaration may be overridden; prefer `\scriptsize` for longer bibliographies.
  - Top-align reference frames, including every continuation page of a multi-page bibliography.
 
 
