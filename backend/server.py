from email_validator import validate_email, EmailNotValidError
from urllib import response
from flask import Flask, Response, request, redirect, flash, render_template, url_for, send_from_directory
from markupsafe import escape
import os
import numpy as np
import cv2
import torch
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import cv2
import csv
from datetime import datetime

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from io import BytesIO
import base64
from torch.nn import CosineSimilarity


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#face_images = []
class_codes = []
known_face_encodings = []
known_face_names = [] # For now, just append file names as names
image_list = []

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=160, margin=0)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def user_imgurls():
    user_url_list = []
    with open('users.csv') as f:
        reader = csv.reader(f)
        users_csv_data = list(reader)
        header = users_csv_data[0]
        rows = users_csv_data[1:]

        for i in range(len(rows)):
            # Add urls from user
            user_urls = rows[i][header.index('imgUrls')].split(",")
            user_url_list.extend(user_urls)
    return user_url_list


def get_images_embeddings():

    #url_list = user_imgurls()
    url_list = os.listdir(UPLOAD_FOLDER)

    for url in url_list:
        print("URL " + url)
        suffix = url.split('.')[-1]
        prefix = url.split('.')[0]
        if suffix == "npy":
            print('added')
            known_face_encodings.append(np.load(os.path.join(UPLOAD_FOLDER, url)))
        else:
            image_list.append(os.path.join(UPLOAD_FOLDER, url))
        if prefix not in known_face_names:
                known_face_names.append(prefix)


app = Flask(__name__, static_folder='../frontend/build')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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


def user_emails_for_class_code(class_code):
    user_email_list = []
    with open('users.csv') as f:
        reader = csv.reader(f)
        users_csv_data = list(reader)
        header = users_csv_data[0]
        rows = users_csv_data[1:]

        for i in range(len(rows)):
            class_list = rows[i][header.index('classes')].split(",")
            if (class_code in class_list):
                user_email = rows[i][header.index('email')]
                user_email_list.append(user_email)
    return user_email_list



@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            prefix = filename.split(".")[0]
            desired_path_img = os.path.join(UPLOAD_FOLDER, filename)
            desired_path_embed = os.path.join(UPLOAD_FOLDER, f'{prefix}.npy')
            
            # Generate and save the embedding
            img = Image.open(file).convert('RGB')
            # Get cropped and prewhitened image tensor
            img_cropped = mtcnn(img)

            if img_cropped is not None:
                # Remove existing files if name conflicts
                if os.path.exists(desired_path_img):
                    os.remove(desired_path_img)
                    if os.path.exists(desired_path_embed):
                        os.remove(desired_path_embed)
                file.save(desired_path_img)

                # Calculate embedding (unsqueeze to add batch dimension)
                img_embedding = resnet(img_cropped.unsqueeze(0))
                np.save(desired_path_embed, img_embedding.detach().numpy())
            
            else:
                print('Embedding failed')
                flash('Embedding failed')

    return redirect('/upload')

### TODO: implement
def mark_as_present(name):
    pass



### Detect faces from image endpoint
# request data includes image and classcode in one string
@app.route('/api/detect/', methods=['POST', 'GET'], defaults={'class_code': None})
@app.route('/api/detect/<class_code>', methods=['POST', 'GET'])
@cross_origin()
def detect_face_from_img(class_code):
    try:
        if request.method == 'POST':
            # print(request.form['image'])
            # img = Image.open(BytesIO(base64.b64decode(request.form['image'])))
            file = request.form['image']
            starter = file.find(',')
            image_data = file[starter+1:]
            image_data = bytes(image_data, encoding="ascii")
            img = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')

            img_cropped = mtcnn(img)
            # Calculate embedding (unsqueeze to add batch dimension)
            img_embedding = resnet(img_cropped.unsqueeze(0))

            # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            distance = None
            cos = CosineSimilarity()
            min_idx = None
            get_images_embeddings() # don't mess with class code
            print(f"LEN:  {len(known_face_encodings)}")
            for idx in range(len(known_face_encodings)):
                cur_embedding = torch.from_numpy(known_face_encodings[idx])
                output = cos(cur_embedding, img_embedding)[0].item()
                if distance is None or output < distance:
                    distance = output
                    min_idx = idx
            if min_idx is not None:
                name = known_face_names[min_idx]
                mark_as_present(name)
                return name
            else:
                return 'FAILED'
    except Exception as e:
        print('error occurred during detection')
        print(e)
        return 'FAILED'


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
    return redirect(STUDENT_HOME)

@app.route('/api/get-attendance', methods=['GET'])
def get_attendance():
    # TODO
    return redirect(TEACHER_HOME)

@app.route('/api/get-classes', methods=['GET'])
def get_classes():
    # TODO
    return redirect(TEACHER_HOME)

if __name__ == "__main__":
    app.run(debug=True)
