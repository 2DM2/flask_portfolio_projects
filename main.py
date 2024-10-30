from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from cnn_melanoma.cnn_melanoma import cnn_melanoma_bp

app = Flask(__name__)

app.register_blueprint(cnn_melanoma_bp, url_prefix='/cnn_melanoma')


    
if __name__ == "__main__":
    app.run(debug=True, port=5000) # set debug=False before production use

