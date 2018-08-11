import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = '/share/openvpnclient'


@application.route('/', methods=['GET', 'POST'])
def root():
    return '''
        <!doctype html>
        <title>Upload the certificates</title>
        <h1>Upload new File</h1>
        <form method="post" action="upload/" enctype="multipart/form-data">
          <p><input type="file" name="file" multiple>
             <input type="submit" value="Upload">
        </form>
        '''


@application.route('/upload/', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        files = request.files.getlist('file')
        # if user does not select file, browser also
        # submit a empty part without filename
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:

                filename = os.path.join(application.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                print("Save file {file} into {path}".format(file=file, path=filename))
                file.save(filename)
        return redirect(url_for('root'))
