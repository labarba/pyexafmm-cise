#!/bin/bash
pdflatex pyexafmm.tex
bibtex pyexafmm
pdflatex pyexafmm.tex
pdflatex pyexafmm.tex