from flask import Flask, render_template, request
from flask_codemirror import CodeMirror
from flask_wtf import Form
from flask_codemirror.fields import CodeMirrorField
from wtforms.fields import SubmitField
from latexEditor.setup import app,default_body
import os, subprocess


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class textForm(Form):
    header = CodeMirrorField(language='stex',config={'lineNumbers':'true','lineWrapping':'true'} )
    body = CodeMirrorField(language='stex',config={'lineNumbers' : 'true','lineWrapping':'true'})
    files = CodeMirrorField(language='none',config={'lineNumbers' : 'false','lineWrapping':'true'})
    submit = SubmitField('Submit')

@app.route("/",methods = ['GET', 'POST'])
def index():
    print 'start of index'
    form = textForm()
    if request.method == 'POST':
        texSave(form);
    form.header.data = texGet();
    form.body.data = default_body;
    if form.validate_on_submit():
        print 'form was validated'
    #texCompile(form)
    return render_template('index.html', form=form)

def texSave(Obj):
    ''' save text fields to a local file'''
    headName = os.path.join(BASE_DIR,'latexEditor/static/headFile.txt')
    headFile = open(headName,'w')
    headFile.write(Obj.header.data)

def texGet():
    ''' returns the text fields from local file'''
    headName = os.path.join(BASE_DIR,'latexEditor/static/headFile.txt')
    headFile = open(headName,'r')
    headText = headFile.read();
    print headText
    return headText


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
