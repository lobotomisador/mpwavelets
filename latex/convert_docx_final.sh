#!/bin/bash

echo "Converting Markdown to DOCX with Times New Roman formatting..."

# Convert to DOCX with Times New Roman and specific formatting
pandoc md/wavelets-part1.md \
  --from markdown \
  --to docx \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --citeproc \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --list-of-figures \
  --list-of-tables \
  --variable=mainfont:"Times New Roman" \
  --variable=fontsize:9pt \
  --variable=linestretch:2.0 \
  --variable=geometry:margin=1in \
  -o wavelets-part1.docx

echo "DOCX file generated: wavelets-part1.docx"
echo ""
echo "Conversion complete!"
echo ""
echo "The document has been created with basic formatting."
echo "To achieve the exact formatting you requested, please:"
echo ""
echo "1. Open wavelets-part1.docx in Microsoft Word"
echo "2. Select all text (Ctrl+A)"
echo "3. Set font to Times New Roman, 9pt"
echo "4. Set double spacing (Line and Paragraph Spacing > 2.0)"
echo "5. For headers:"
echo "   - Level 1: 11pt, Bold"
echo "   - Level 2: 10pt"
echo "   - Level 3: 10pt"
echo "6. Add line numbers: Layout tab > Line Numbers > Continuous"
echo ""
echo "Alternative: Use the 'Styles' pane to modify heading styles globally." 