from email_validator import validate_email, EmailNotValidError
from urllib import response
from flask import Flask, Response, request, redirect, flash, render_template, url_for, send_from_directory
from markupsafe import escape
import os
import numpy as np
import cv2
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
known_face_encodings = []
known_face_names = [] # For now, just append file names as names

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=160, margin=0)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()

def make_images_and_encodings():

    for class_code_dir in os.listdir('uploads'):
        for file in os.listdir(os.path.join(UPLOAD_FOLDER, class_code_dir)):
            
            """
            loaded_image = face_recognition.load_image_file(file)
            face_images.append(loaded_image)
            known_face_encodings.append(face_recognition.face_encodings(loaded_image)[0])
            known_face_names.append(file) # CHANGE TO BE ACTUAL NAMES SOMEHOW
            """

            img = Image.open(os.path.join(UPLOAD_FOLDER, class_code_dir, file))
            # Get cropped and prewhitened image tensor
            img_cropped = mtcnn(img)

            if img_cropped is not None:

                # Calculate embedding (unsqueeze to add batch dimension)
                img_embedding = resnet(img_cropped.unsqueeze(0))
                known_face_encodings.append(img_embedding)
                known_face_names.append(file)
            else:
                print('got NONE embedding')

make_images_and_encodings()



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



### Detect faces from image endpoint
# request data includes image and classcode in one string
@app.route('/api/detect/', methods=['POST', 'GET'], defaults={'class_code': None})
@app.route('/api/detect/<class_code>', methods=['POST', 'GET'])
@cross_origin()
def detect_face_from_img(class_code):
    if request.method == 'POST':
        # print(request.form['image'])
        # img = Image.open(BytesIO(base64.b64decode(request.form['image'])))
        file = request.form['image']
        starter = file.find(',')
        image_data = file[starter+1:]
        image_data = bytes(image_data, encoding="ascii")
        img = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')

        """
        nparr = np.fromstring(request.data, np.uint8) # convert string of image data to uint8
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) # decode image
        #face_encoding = face_recognition.face_encodings(img)[0] # Get first match only
        """
        img_cropped = mtcnn(img)
        # Calculate embedding (unsqueeze to add batch dimension)
        img_embedding = resnet(img_cropped.unsqueeze(0))

        # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        distance = None
        cos = CosineSimilarity()
        min_idx = None
        for idx in range(len(known_face_encodings)):
            cur_embedding = known_face_encodings[idx]
            output = cos(cur_embedding, img_embedding)[0].item()
            if distance is None or output < distance:
                distance = output
                min_idx = idx
        if min_idx is not None:
            name = known_face_names[min_idx]
            return name
        else:
            return 'FAILED'

        
        """
        name = ""
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_idx = np.argmin(face_distance)
        if matches[best_match_idx]:
            name = known_face_names[best_match_idx]
        if name in known_face_names:
            print(name +" is here")
        
            return Response("{'foundUser':" + name + "}", status=200, mimetype='application/json')
        """
    # return Response("{'foundUser':'None'}", status=404, mimetype='application/json')


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
