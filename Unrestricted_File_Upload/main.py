import os

from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        file = request.files['fileInput']
        cwd = os.getcwd()
        save_path = cwd + '/' + file.filename
        file.save(save_path)
        return render_template('index.html', upload_path=save_path)
    else:
        return redirect('/', code=405)