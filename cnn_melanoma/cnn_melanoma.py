import os
from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from cnn_melanoma.cnn_predict import *

cnn_melanoma_bp = Blueprint('cnn_melanoma_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/cnn_melanoma',    
    url_prefix='/cnn_melanoma'
    )

# @cnn_melanoma_bp.route('/cnn_melanoma')

@cnn_melanoma_bp.route('/')
def home():
    return render_template('/cnn_melanoma/home.html')


# ---------------------- upload file ------------------------
# define upload folder
#cnn_melanoma_bp.config['UPLOAD_FOLDER'] = '/uploads'
upload_folder = 'cnn_melanoma/static/cnn_melanoma/uploads/'

# define model
#cnn_melanoma_bp.config['MODEL'] = '/static/models/model_3_3_best.pkl'
model = 'cnn_melanoma/static/cnn_melanoma/models/model_3_3_best.pkl'

# restrict file size
#cnn_melanoma_bp.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB
max_content_length = 20 * 1024 * 1024  # 20 MB

# restrict to only images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@cnn_melanoma_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        #--------------user upload image---------------#
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('File Does Not Exist')
            return redirect(request.url)
        file = request.files['file']
        # if the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No File Selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):            
            f = request.files['file']
            f.save(upload_folder + secure_filename(f.filename))
            img_path = upload_folder + f.filename
            user_img = secure_filename(f.filename)

            #secure_filename = secure_filename(file.filename)
            #file_secure = file.save(os.path.join(upload_folder, secure_filename)) 

        try:
            # make prediction                
            prediction = make_prediction(model, preprocess_image(img_path)) 
            return render_template('/cnn_melanoma/home.html', prediction=prediction, user_img=user_img)

        except ValueError:
            return "Error, please go back and try again."
        
        pass
    pass




"""
@cnn_melanoma_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' in request.files:
        file = request.files['file']
        # error handling - allowable file type
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        # save file 
            # join filename and folder path
            secure_filename = secure_filename(file.filename)
            file.save(os.path.join(cnn_melanoma_bp.config['UPLOAD_FOLDER'], secure_filename))           
            return 'File uploaded successfully'    

    return 'File upload failed'
"""

# ---------------- error handler -------------------
"""
from flask import Flask, abort, make_response, jsonify

# error handling - file too large
from werkzeug.exceptions import RequestEntityTooLarge

@cnn_melanoma_bp.errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return 'File is too large', 413

@cnn_melanoma_bp.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)


# error handling - missing file
if 'file' not in request.files:
    return 'No file part in the request', 400
# error handling - empty file name
file = request.files['file']
if file.filename == '':
    return 'No selected file', 400
# error handling - disallowed file type
if file and not allowed_file(file.filename):
    return 'File type not allowed', 400
# error handling - file save error
try:
    file.save(os.path.join(cnn_melanoma_bp.config['UPLOAD_FOLDER'], filename))
except Exception as e:
    return f'Error saving file: {str(e)}', 500       
"""


