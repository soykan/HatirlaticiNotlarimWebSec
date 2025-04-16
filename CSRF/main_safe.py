from flask import Flask, render_template, request, redirect
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)


# SECRET KEY required for CSRF protection mechanism
app.config.from_mapping(SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf') # https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY

# CSRF Protection initalize
csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index_safe.html')
    elif request.method == 'POST':

        '''
        It's a simple example
        Store passwords in a database while using secure hashing algorithm
        '''
        if request.form['currentPassword'] == 'current-password-123':
        
            # check input fields empty or not in a real app
            p1 = request.form['password1']
            p2 = request.form['password2']

            if p1 == p2:
                return render_template('index_safe.html', result='Password changed.')
            else:
                return render_template('index_safe.html', result='Two input fields must contain same password to change it.')

        else:
            return render_template('index_safe.html', result='Current password does not match.')

    else:
        return redirect('/', code=405)