######################
# UNDER CONSTRUCTION #
######################


import os
import random
import string

from flask import Flask, request, render_template, redirect, send_from_directory

from flask_wtf.csrf import CSRFProtect

import magic


app = Flask(__name__, instance_relative_config=True)

app.config['UPLOAD_FOLDER'] = os.getcwd() + '/files/' # You may want to change the path instead of storing them in files directory 

# SECRET KEY required for CSRF protection mechanism
app.config.from_mapping(SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf') # https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY

# Max file size 16 Megabyte (That doesn't affected by a changed Content-Length header)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 

# CSRF Protection initalize
csrf = CSRFProtect(app) # -----


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_FILE_TYPES = {'image/jpeg', 'image/jpg', 'image/png'}

@app.route('/images/<name>', methods=['GET'])
def imageViewPage(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)



@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'GET':
        return render_template('index_safe.html')   
    elif request.method == 'POST':
        file = request.files['fileInput']
        is_allowed_ext = ext_check(file.filename)
        if not is_allowed_ext:
            extension_error = 'Valid file extension types are' + str([ext for ext in ALLOWED_EXTENSIONS])
            return render_template('index_safe.html', error=extension_error)


        if not file_type_check(file):
            file_type_error = 'File type does not match with any of these:' + str([type_of_file for type_of_file in ALLOWED_FILE_TYPES])
            return render_template('index_safe.html', error=file_type_error)


        cwd = os.getcwd()
        try:       
            os.mkdir(cwd + '/files')
        except FileExistsError:
            pass
        extension_of_file = get_extension(file.filename)
        filename = filename_generator(extension_of_file)
        save_path = app.config['UPLOAD_FOLDER'] + filename
        while os.path.exists(save_path):
            filename = filename_generator(extension_of_file)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.stream.seek(0) # Kaynak: https://github.com/pallets/werkzeug/issues/1666
        file.save(save_path)
        
        return redirect('/images/' + filename)
        #return render_template('index_safe.html', upload_path=save_path)
    else:
        return redirect('/', code=405)


def get_extension(filename):
    ext_start_index = filename.rindex('.') + 1
    extension = filename[ext_start_index:]
    return extension 

def ext_check(filename):
    extension = get_extension(filename)
    if extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def filename_generator(extension):
    rand_file_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return rand_file_name + '.' + extension
    # Alternative olarak secure_filename()
    # https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.utils.secure_filename


def file_type_check(file):
    file_type = magic.from_buffer(file.read(), mime=True)
    if file_type in ALLOWED_FILE_TYPES:
        return True
    return False




'''
FROM OWASP CheatSheet
In short, the following principles should be followed to reach a secure file upload implementation:

List allowed extensions. Only allow safe and critical extensions for business functionality
Ensure that input validation is applied before validating the extensions.

Validate the file type, don't trust the Content-Type header as it can be spoofed

Change the filename to something generated by the application

Set a filename length limit. Restrict the allowed characters if possible

Set a file size limit

Only allow authorized users to upload files

Store the files on a different server. If that's not possible, store them outside of the webroot

In the case of public access to the files, use a handler that gets mapped to filenames inside the application (someid -> file.ext)

Run the file through an antivirus or a sandbox if available to validate that it doesn't contain malicious data

Run the file through CDR (Content Disarm & Reconstruct) if applicable type (PDF, DOCX, etc...)

Ensure that any libraries used are securely configured and kept up to date

Protect the file upload from CSRF attacks
'''
