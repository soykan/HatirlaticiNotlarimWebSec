from flask import Flask, render_template, request, redirect, make_response


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        p1 = request.form['password1']
        p2 = request.form['password2']
        if p1 == p2:
            r = make_response(render_template('index.html', result='Password changed.'))
            r.headers.set('Access-Control-Allow-Origin', "*")
            return r

        else:
            r = make_response(render_template('index.html', result='Two input fields must contain same password to change it.'))
            r.headers.set('Access-Control-Allow-Origin', "*")
            return r
    else:
        return redirect('/', code=405)