from markupsafe import escape
from flask import Flask 
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app=Flask(__name__,template_folder='template')

from routes import * 

if __name__ == '__main__':
    app.run(debug=True)
