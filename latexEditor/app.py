from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_codemirror import CodeMirror
from flask_wtf import Form
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from initFields import default_head
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
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
);
# Initialize database
db = SQLAlchemy(app)
# Initialize codemirror
codemirror = CodeMirror(app)
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

    def __init__(self, name, header):
        self.name = name
        self.header = header

    def __repr__(self):
        return '<db Model name: %r>' % self.name

def texCompile(Obj):
    inTag   = '~I~{'
    outTag  = '~O~{'
    replTag = '\lstinputlisting{'

    # orginize file paths with their id's
    tempArray = Obj.files.data.splitlines()
    pathArray = []
    # each line contains an id and a path to a file
    for line in tempArray:
        temp = line.split('::')
        pathArray.append(temp)

    for tag,filePath in pathArray:
        tag = str(tag); filePath = str(filePath);
        # run the files code and store it in an output file
        fileOutput = subprocess.check_output(['python',filePath])

        # make all str replacements
        outLine = outTag + tag + '}'
        outRepl = '\\begin{lstlisting}\n' + fileOutput + '\n\\end{lstlisting}\n'
        print 'outLine',outLine
        print 'outRepl',outRepl
        # replace output tag blocks with file output
        Obj.body.data=Obj.body.data.replace(outLine,outRepl)
        # replace input tag with filePath
        Obj.body.data=Obj.body.data.replace(tag,filePath)
        # replace input block with lstinputlisting
        Obj.body.data=Obj.body.data.replace(inTag,replTag)
    print 'obj.body after str rep: ',Obj.body.data
    # put blocks together into a file
    fTexName = os.path.join(BASE_DIR,'latexEditor/static/fOut.tex')
    print 'tex file location: ',fTexName
    fTex = open(fTexName,'w')
    fTex.write(Obj.header.data)
    fTex.write(Obj.body.data)
    fTex.close()
    # now compile tex file into pdf
    os.chdir('latexEditor/static/');
    os.system('pdflatex fOut.tex')
    os.chdir('../../');
    os.system('pwd')
# ...

@app.route("/",methods = ['GET', 'POST'])
def index():
    print 'start of index'
    form = textForm()
    textModel = textIn.query.filter_by(name='test').first();
    if request.method == 'POST':
        print 'method is a POST'
        # update model if it exists
        print 'before: ',textModel.header
        textModel.header = form.header.data 
        print 'after: ',textModel.header
        db.session.commit()
    else:
        print 'method is a GET'
        form.header.data = textModel.header
    #if form.validate_on_submit():
    #    print 'form was validated'
    #texCompile(form)
    return render_template('index.html', form=form)


if __name__=='__main__':
    db.drop_all()
    db.create_all()
    db.session.add(textIn('test',default_head))
    db.session.commit()
    app.run(host='0.0.0.0',port=5950,debug=True)
