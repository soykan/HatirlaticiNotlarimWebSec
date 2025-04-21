from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/api/v1/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    typed_pass_1 = data['password1']
    typed_pass_2 = data['password2']
    if typed_pass_1 == typed_pass_2:
        r = jsonify({'result': 'success'})
        r.headers.set('Access-Control-Allow-Origin', "*")
        r.headers.set('Cross-Origin-Resource-Policy', 'cross-origin')
        return r
    else:
        r = jsonify({'result': 'fail'})
        r.headers.set('Access-Control-Allow-Origin', "*")
        r.headers.set('Cross-Origin-Resource-Policy', 'cross-origin')
        return r
