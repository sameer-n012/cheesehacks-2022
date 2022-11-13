from email_validator import validate_email, EmailNotValidError
from urllib import response
from flask import Flask, request, redirect, flash, render_template, url_for, send_from_directory, Response
from markupsafe import escape
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder='../frontend/build')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

STUDENT_HOME = '/student'
TEACHER_HOME = '/admin'


# Serve up frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_frontend(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        print('showing index.html')
        return send_from_directory(app.static_folder, 'index.html')


# Create class endpoint
@app.route('/api/create-class', methods=['GET', 'POST'])
def create_class():
    if 'class_code' not in request.form:  # class_code must match name attribute of html form
        flash('No class code')
        return redirect(request.url)
    class_code = request.form['class_code']
    class_path = os.path.join(UPLOAD_FOLDER, class_code)
    if not os.path.exists(class_path):
        os.mkdir(class_path)
    return redirect('/class')


### Create class endpoint 2
@app.route('/api/create-class2', methods=['GET', 'POST'])
def create_class2():
    class_name = request.data.decode('utf-8')
    class_code = generate_class_code(class_name)
    print("Class " + class_name + " with code " + class_code + " was created")

    return redirect(TEACHER_HOME)

### Create a unique class code # TODO make it unique
def get_class_code(class_name):
    return hash(class_name) % (10**10)

### Student upload image endpoint
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # Check if the requst has the class code
        if 'class_code' not in request.form:
            flash('No class code')
            return redirect(request.url)
        class_code = request.form['class_code']

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            desired_path = os.path.join(UPLOAD_FOLDER, class_code)
            if not os.path.exists(desired_path):
                flash('Invalid class code')
                return redirect(request.url)
            file.save(os.path.join(desired_path, filename))
            return redirect('/upload')
    return redirect('/upload')


### Email Check route
@app.route('/api/email_check', methods=['GET', 'POST'])
def email_check():
    # print(request.form['email'])
    if 'email' not in request.form:
        pass
    else:
        email = request.form['email']
        if not isEmail:
            return Response("{'message': 'Invalid! Email is not registered'}", 
                status=200, mimetype='application/json')
    # return redirect('/')

 
def isEmail(email):
    try:
      # validate and get info
        v = validate_email(email)
        # replace with normalized form
        email = v["email"] 
        return True
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return False


@app.route('/api/teacher_sign_up', methods=['GET', 'POST'])
def teacher_sign_up():
    return redirect(TEACHER_HOME)

### Join class endpoint
@app.route('/api/join-class', methods=['POST'])
def join_class():
    class_code = request.data.decode('utf-8')
    print('joining class', class_code)
    return redirect(STUDENT_HOME)


@app.route('/api/student_sign_up', methods=['GET', 'POST'])
def student_sign_up():
    return redirect("/Student")


if __name__ == "__main__":
    app.run(debug=True)
