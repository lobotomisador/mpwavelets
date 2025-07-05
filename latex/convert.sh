#!/bin/bash

echo "Converting Markdown to LaTeX..."

# Simple conversion to LaTeX
pandoc md/wavelets-part1.md \
  --from markdown \
  --to latex \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --list-of-figures \
  --list-of-tables \
  --citeproc \
  -o wavelets-part1.tex

echo "LaTeX file generated: wavelets-part1.tex"

echo "Converting to PDF..."

# Convert to PDF
pandoc md/wavelets-part1.md \
  --from markdown \
  --to pdf \
  --bibliography=references.bib \
  --csl=ieee.csl \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --list-of-figures \
  --list-of-tables \
  --pdf-engine=xelatex \
  --citeproc \
  -o wavelets-part1.pdf

echo "PDF file generated: wavelets-part1.pdf"
echo "Conversion complete!" 