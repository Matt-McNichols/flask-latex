from latexEditor import app
import os

if __name__=='__main__':
    app.run(debug=True)

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
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    headName = os.path.join(BASE_DIR,'flask-latex/latexEditor/static/headFile.txt')
    headFile = open(headName,'w')
    headFile.write(default_head)
