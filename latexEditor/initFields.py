#!/usr/bin/python

default_head = '''
\\documentclass{report}
\\usepackage{geometry}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{hyperref}
\\usepackage{graphicx}
\\usepackage{float}
\\usepackage{amsmath}
\\usepackage{subcaption}
\\usepackage{caption}
\\usepackage{mathtools}
\\usepackage{listings}

\\graphicspath{ {images/}}
\\hypersetup{
colorlinks=true,
linktoc=all,
linkcolor=blue!60,
}
\\geometry{legalpaper, portrait, margin=0.5in}
\\lstdefinestyle{custom}{
  basicstyle=\small\\ttfamily,
  columns=flexible,
  breaklines=true,
  frame=single,
  language=Python ,
  keepspaces=true,
  backgroundcolor=\color{gray!20},
  keywordstyle=\\bfseries\color{purple!70!black},
  identifierstyle=\color{black},
  stringstyle=\color{blue},
  commentstyle=\color{green!40!black}
}

\\lstset{style=custom}

\\title{Test Title}
\\author{Matt McNichols}
\\date{\\today}

\\DeclarePairedDelimiter\\floor{\lfloor}{\\rfloor}
'''

default_body = '''
\\begin{document}

\\maketitle
\\tableofcontents

\\chapter{random lists}
\\section{Introduction}
\href[page=50]{https://drive.google.com/open?id=0B47Em9Je9ElOdGZEaTc2VnlCYUE}{link to algorithms book}\\
here is some text under the link\\
~O~{testFile}
here is more text under the link
\\begin{description}
    \\item[Master Method]\hfill
    \\begin{itemize}
        \\item chapter 4 in book
        \\item $f(n) = \Omega{n}$
        \\item another item
        \\item hello there
    \\end{itemize}

    \\item[Analysis of Quicksort]\hfill
    \\begin{itemize}
        \\item worst case vs average case
        \\item chapter 7
    \\end{itemize}

    \\item[Partitioning Schemes]\hfill
    \\begin{itemize}
        \\item quick selection
        \\item median of median
        \\item chapter 9
    \\end{itemize}

\\end{description}

\\section{testing}
lets see if this will work\\
this is a test to see if updates work\\
~I~{testFile}
another line here\\
there should be two lines between block listings\\
~O~{testFile}
\section{Number Two Test}
here is some text before the number two file\\
\\end{document}
'''
default_file = 'testFile::/home/matt/mattGitHub/flask-latex/latexEditor/static/testFile.py'
