#!/bin/bash

echo "Converting Markdown to DOCX with advanced formatting..."

# Check if python-docx is available
if python3 -c "import docx" 2>/dev/null; then
    echo "Creating custom reference document..."
    python3 create_reference_docx.py
    REFERENCE_DOC="reference.docx"
else
    echo "python-docx not available, using default reference document..."
    pandoc --print-default-data-file reference.docx > reference.docx
    REFERENCE_DOC="reference.docx"
fi

# Convert to DOCX with custom formatting
pandoc md/wavelets-part1.md \
  --from markdown \
  --to docx \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --citeproc \
  --reference-doc=$REFERENCE_DOC \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --list-of-figures \
  --list-of-tables \
  -o wavelets-part1.docx

echo "DOCX file generated: wavelets-part1.docx"

# Clean up temporary file
rm reference.docx

echo "Conversion complete!"
echo ""
echo "The document has been created with:"
echo "- Times New Roman font"
echo "- 11pt bold headers"
echo "- 10pt subheaders" 
echo "- 9pt normal text"
echo "- Double spacing"
echo ""
echo "To add line numbers in Word:"
echo "1. Open the document in Microsoft Word"
echo "2. Go to Layout tab"
echo "3. Click 'Line Numbers'"
echo "4. Select 'Continuous' or your preferred option" 