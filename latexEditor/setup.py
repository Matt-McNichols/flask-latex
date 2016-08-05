from flask import Flask
from flask_codemirror import CodeMirror

SECRET_KEY = 'secret!'
# mandatory
CODEMIRROR_LANGUAGES = [ 'htmlembedded','python','stex']
# optional
CODEMIRROR_THEME = '3024-day'
CODEMIRROR_ADDONS = (
                    ('display','placeholder'),
                    )
app = Flask(__name__, static_url_path='')
app.config.from_object(__name__)
codemirror = CodeMirror(app)

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
~I~{secondFile}
the output of the second file will be below\\
~O~{secondFile}
this is some text under the output of the second file
\\end{document}
'''
