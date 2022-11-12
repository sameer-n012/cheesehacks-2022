from urllib import response
from flask import Flask, request, redirect, flash, render_template, url_for, send_from_directory
from markupsafe import escape
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, static_folder = '../react-frontend/build')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def show_frontend(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        print('showing index.html')
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug = True)