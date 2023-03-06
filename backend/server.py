from email_validator import validate_email, EmailNotValidError
from urllib import response
from flask import Flask, Response, request, redirect, flash, render_template, url_for, send_from_directory, jsonify
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
import pandas as pd

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from io import BytesIO
import base64
from torch.nn import CosineSimilarity
import pandas as pd
from html_error_outputs import *

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
        img_path = os.path.join(UPLOAD_FOLDER, url)
        if img_path not in image_list and suffix != "npy":
            known_face_names.append(prefix)
            known_face_encodings.append(np.load(os.path.join(UPLOAD_FOLDER, prefix + ".npy")))
            image_list.append(os.path.join(UPLOAD_FOLDER, url))


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
# @app.route('/api/create-class', methods=['GET', 'POST'])
# def create_class():
#     if 'class_code' not in request.form:  # class_code must match name attribute of html form
#         flash('No class code')
#         return redirect(request.url)
#     class_code = request.form['class_code']
#     class_path = os.path.join(UPLOAD_FOLDER, class_code)
#     if not os.path.exists(class_path):
#         os.mkdir(class_path)
#     return redirect('/class')


### Create class endpoint 2
@app.route('/api/create-class2', methods=['POST'])
def create_class2():
    class_name = request.data.decode('utf-8')
    userid = request.args.get('userid', None)
    class_code = generate_class_code(class_name)
    f = open("./classes.csv", "a")
    f.write(str(class_code) + "," + class_name.replace(",", "") + ",,,0\n")
    f.close()
    print("Class " + class_name + " with code " + str(class_code) + " was created")
    addToClass(userid, str(class_code))

    return str(class_code)

### Create a unique class code # TODO make it unique
def generate_class_code(class_name):
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
            similarity = None
            cos = CosineSimilarity()
            max_idx = None
            get_images_embeddings() # don't mess with class code
            for idx in range(len(known_face_encodings)):
                cur_embedding = torch.from_numpy(known_face_encodings[idx])
                output = cos(cur_embedding, img_embedding)[0].item()
                if similarity is None or output > similarity:
                    similarity = output
                    max_idx = idx
            if max_idx is not None:
                name = known_face_names[max_idx]
                addToPresentList(name, class_code)
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
    db = pd.read_csv('users.csv')

    # Redirect to same page if request does not contain email
    if 'email' not in request.form:
        return redirect('/')

    email = request.form['email']
    # Check if email is valid 
    if not isEmail(email):
        return email_invalid_error_page

    # Check if email is in database
    if not isRegistered(email, db):
        return email_unregistered_error_page
    
    # Redirect to corresponding page
    userType = db.loc[db['email'] == email, 'userType'].values[0]
    print(userType)
    if userType == 'student':
        return redirect(STUDENT_HOME)
    elif userType == 'teacher':
        return redirect(TEACHER_HOME)
    else:
        return redirect('/')


def isRegistered(email, db):
    # Check if email is in database
    print(db)
    if email in db['email'].values:
        return True
    return False


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
    db = pd.read_csv('users.csv')

    if 'email' not in request.form:
        return redirect('/')
    email = request.form['email']
    # Check if email is valid
    if not isEmail(email):
        return email_invalid_error_page

    if isRegistered(email, db):
        return email_registered_error_page
    else:
        # Add teacher to database
        db = db.append({'email': email, 'userType': 'teacher', 'imgUrl': email.split("@")[0]}, ignore_index=True)
        db.to_csv('users.csv', index=False)
        return redirect(TEACHER_HOME)

### Join class endpoint
@app.route('/api/join-class', methods=['POST'])
def join_class():
    class_code = request.data.decode('utf-8')
    userid = request.args.get('userid', None)
    print('joining class', class_code)

    a = addToClass(userid, class_code)
    addToAbsentList(userid, class_code)
    return a


def addToClass(student, class_code):
    classDF = pd.read_csv('./classes.csv', keep_default_na=False)
    userDF = pd.read_csv('./users.csv', keep_default_na=False)
    print(classDF)

    # if class_code not in classDF['code'].values:
    #     raise Exception("? ", class_code)

    class_set = set(userDF.loc[userDF['email'] == student, 'classes'].iloc[0].split(","))
    if("" in class_set):
        class_set.remove("")
    class_set.add(class_code)
    # Change class list a student is in by adding the class code given
    userDF.loc[userDF['email'] == student, 'classes'] =  ",".join(class_set)

    userDF.to_csv('./users.csv', index=False)
    print("Class " + str(class_code) + " was joined")

    return str(class_code)

def addToPresentList(student, class_code):
    classDF = pd.read_csv('./classes.csv', keep_default_na=False)
    classDF['code'] = classDF['code'].astype(str)

    absent_set = set(classDF.loc[classDF['code'] == class_code, 'absent'].values[0].split(','))
    present_set = set(classDF.loc[classDF['code'] == class_code, 'present'].values[0].split(','))
    if("" in present_set):
        present_set.remove("")
    if("" in absent_set):
        absent_set.remove("")
    
    for student_email in absent_set:
        if student_email.startswith(student):
            absent_set.remove(student)
            present_set.add(student)
            break

    classDF.loc[classDF['code'] == class_code, 'present'] = ",".join(present_set)
    classDF.loc[classDF['code'] == class_code, 'absent'] = ",".join(absent_set)

    classDF.to_csv('./classes.csv', index=False)


def addToAbsentList(student, class_code):
    classDF = pd.read_csv('./classes.csv', keep_default_na=False)
    classDF['code'] = classDF['code'].astype(str)

    # Add a given student to the absent list of a given class
    # And if they're on the present list, remove them from there
    absent_set = set(classDF.loc[classDF['code'] == class_code, 'absent'].values[0].split(','))

    present_set = set(classDF.loc[classDF['code'] == class_code, 'present'].values[0].split(','))
    if("" in present_set):
        present_set.remove("")
    if("" in absent_set):
        absent_set.remove("")

    if student in present_set:
        present_set.remove(student)
        present_set = ",".join(present_set)
        classDF.loc[classDF['code'] == class_code, 'present'] = present_set
    else:
        classDF.loc[classDF['code'] == class_code, 'class_size'] = len(present_set) + len(absent_set) + 1
    
    absent_set.add(student)
    absent_set = ",".join(absent_set)
    classDF.loc[classDF['code'] == class_code, 'absent'] = absent_set
    classDF.to_csv('./classes.csv', index=False)

def moveAllToAbsent(class_code):
    classDF = pd.read_csv('./classes.csv', keep_default_na=False)
    classDF['code'] = classDF['code'].astype(str)

    absent_set = set(classDF.loc[classDF['code'] == class_code, 'absent'].values[0].split(','))
    present_set = set(classDF.loc[classDF['code'] == class_code, 'present'].values[0].split(','))
    if("" in present_set):
        present_set.remove("")
    if("" in absent_set):
        absent_set.remove("")
    absent_set = absent_set.union(present_set)

    absentees = ",".join(absent_set)
    classDF.loc[classDF['code'] == class_code, 'present'] = ""
    classDF.loc[classDF['code'] == class_code, 'absent'] = absentees

    classDF.to_csv('./classes.csv', index=False)


@app.route('/api/student_sign_up', methods=['GET', 'POST'])
def student_sign_up():
    db = pd.read_csv('users.csv')

    if 'email' not in request.form:
        return redirect('/')
    
    email = request.form['email']
    # Check if email is valid
    if not isEmail(email):
        return email_invalid_error_page
    
    # Check if email is in database
    if isRegistered(email, db):
        return email_registered_error_page
    else:
        # Add teacher to database
        db = db.append({'email': email, 'userType': 'student', 'imgUrl': email.split("@")[0]}, ignore_index=True)
        db.to_csv('users.csv', index=False)
        return redirect(STUDENT_HOME)

@app.route('/api/get-attendance', methods=['GET'])
def get_attendance():
    # TODO
    classid = request.args.get('classid', None)
    print(classid)
    classDF = pd.read_csv('./classes.csv', keep_default_na=False)
    classDF['code'] = classDF['code'].astype(str)
    presentlist = classDF.loc[classDF['code'] == classid].iloc[0]['present'].split(",")
    absentlist = classDF.loc[classDF['code'] == classid].iloc[0]['absent'].split(",")
    print(presentlist, absentlist)
    out = "email,attendance\n"
    for s in presentlist:
        if s != "":
            out += s + "," + "Present\n"
    for s in absentlist:
        if s != "":
            out += s + "," + "Absent\n"
    return out


@app.route('/api/get-classes', methods=['GET'])
def get_classes():
    # TODO
    userid = request.args.get('userid', None)
    print(userid)
    userDf = pd.read_csv('./users.csv', keep_default_na=False)
    classDF = pd.read_csv('./classes.csv', keep_default_na=False)
    classDF['code'] = classDF['code'].astype(str)
    classes = str(userDf.loc[userDf['email'] == userid].iloc[0]['classes']).split(",")
    print(classes)
    if len(classes) == 1 and classes[0] == "":
        return jsonify([])
    elif len(classes) == 0:
        return jsonify([])

    out = []
    for c in classes:
        if c == "":
            continue
        print(classDF.loc[classDF['code'] == c])
        cline = classDF.loc[classDF['code'] == c].iloc[0]
        num_present = len(cline['present'].split(","))
        if "" in cline['present'].split(","):
            num_present -= 1
        out.append({
            "code": cline["code"],
            "name": cline["name"],
            "present": bool(userid in cline["present"].split(",")),
            "num_present": min(num_present, int(cline["class_size"])),
            "class_size": int(cline["class_size"])
        })
    print(classes)
    print(out)
    return jsonify(out)


if __name__ == "__main__":
    app.run(debug=True)
