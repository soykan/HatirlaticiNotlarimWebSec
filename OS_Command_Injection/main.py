import subprocess 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def mainPage():
    if request.method == 'POST':
        ipAddress = request.form['ipAddress']
        command = 'ping -c 4 ' + ipAddress 
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        '''
        try:
            output = subprocess.check_output(['ping', '-c', '4', ipAddress]).decode('utf-8')
        except:
            return render_template('index.html', result=['Error while processing your input'])
        '''
        output_lines = output.split('\n')
        return render_template('index.html', result=output_lines)
    elif request.method == 'GET':
        return render_template('index.html')