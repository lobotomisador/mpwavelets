#!/bin/bash

echo "Converting Markdown to DOCX with custom formatting..."

# First, create a simple reference document
pandoc --print-default-data-file reference.docx > reference.docx

# Convert to DOCX with custom formatting
pandoc md/wavelets-part1.md \
  --from markdown \
  --to docx \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --citeproc \
  --reference-doc=reference.docx \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --list-of-figures \
  --list-of-tables \
  --variable=fontsize:9pt \
  --variable=mainfont:"Times New Roman" \
  --variable=linestretch:2.0 \
  -o wavelets-part1.docx

echo "DOCX file generated: wavelets-part1.docx"

# Clean up temporary file
rm reference.docx

echo "Conversion complete!"
echo ""
echo "Note: You may need to manually adjust the following in Word:"
echo "1. Set line numbers (Layout > Line Numbers)"
echo "2. Adjust header sizes:"
echo "   - Level 1 headers: 11pt, Bold"
echo "   - Level 2 headers: 10pt"
echo "   - Normal text: 9pt"
echo "3. Set double spacing (Line and Paragraph Spacing > 2.0)" 