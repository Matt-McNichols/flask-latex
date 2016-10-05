from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_codemirror import CodeMirror
from flask_wtf import Form
from flask_codemirror.fields import CodeMirrorField
from flask_bootstrap import Bootstrap
from wtforms.fields import SubmitField
from initFields import default_head, default_body,default_file
import os, subprocess


# Initialize app
app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'secret!',
    # mandatory
    CODEMIRROR_LANGUAGES = [ 'htmlembedded','python','stex'],
    # optional
    CODEMIRROR_THEME = '3024-day',
    CODEMIRROR_ADDONS = (('display','placeholder'),),
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db',
    SEND_FILE_MAX_AGE_DEFAULT = 0,
);
# Initialize database
db = SQLAlchemy(app)
# Initialize codemirror
codemirror = CodeMirror(app)
Bootstrap(app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class textForm(Form):
    header = CodeMirrorField(language='stex',config={'lineNumbers':'true','lineWrapping':'true'} )
    body = CodeMirrorField(language='stex',config={'lineNumbers' : 'true','lineWrapping':'true'})
    files = CodeMirrorField(language='none',config={'lineNumbers' : 'false','lineWrapping':'true'})
    submit = SubmitField('Submit')

class textIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    header = db.Column(db.Text())
    body = db.Column(db.Text())
    files = db.Column(db.Text())

    def __init__(self, name, header, body, files):
        self.name = name
        self.header = header
        self.body = body
        self.files = files

    def __repr__(self):
        return '<db Model name: %r>' % self.name

def texCompile(Obj):
    inTag   = '~I~{'
    outTag  = '~O~{'
    replTag = '\lstinputlisting{'

    # orginize file paths with their id's
    # each line contains an id and a path to a file
    tempArray = Obj.files.data.splitlines()
    pathArray = []
    for line in tempArray:
        temp = line.split('::')
        pathArray.append(temp)

    # make all str replacements
    texBody = Obj.body.data;
    for tag,filePath in pathArray:
        tag = str(tag); filePath = str(filePath);
        fileOutput = subprocess.check_output(['python',filePath])
        outLine = outTag + tag + '}'
        outRepl = '\\begin{lstlisting}\n' + fileOutput + '\n\\end{lstlisting}\n'
        texBody=texBody.replace(outLine,outRepl)
        texBody=texBody.replace(tag,filePath)
        texBody=texBody.replace(inTag,replTag)

    # put blocks together into a file
    # remove old file if it exists
    fTexName = os.path.join(BASE_DIR,'latexEditor/static/texDoc.tex')
    os.system('rm static/texDoc.tex')
    fTex = open(fTexName,'w')
    fTex.write(Obj.header.data)
    fTex.write(texBody)
    fTex.close()

    # now compile tex file into pdf
    os.chdir('static/');
    os.system('pdflatex texDoc.tex')
    os.chdir('../');
    os.system('pwd')
# ...


@app.route("/bs/")
def bs():
    return render_template('bs/blog/index.html')

# TODO: issue loading the static pdf file every time it changes
# NOTE: to make stable remove the extra_files arg
@app.route("/texEditor/",methods = ['GET', 'POST'])
def index():
    form = textForm()
    textModel = textIn.query.filter_by(name='test').first();

    if request.method == 'POST':
        print 'method was a POST'
        textModel.header = form.header.data 
        textModel.body = form.body.data 
        textModel.files = form.files.data
        db.session.commit()
        texCompile(form)
        return redirect(url_for('index'))
    else:
        print 'method was a GET'
        form.header.data = textModel.header
        form.body.data = textModel.body
        form.files.data = textModel.files
    #texCompile(form)
    return render_template('texEditor.html', form=form)

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        print 'setting chache control'
        response.headers['Cache-Control']='no-store'
    return response

if __name__=='__main__':
    db.drop_all()
    db.create_all()
    db.session.add(textIn('test',default_head,default_body,default_file))
    db.session.commit()
    app.run(host='0.0.0.0',port=5950,debug=True)
