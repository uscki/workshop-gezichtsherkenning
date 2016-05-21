import json, requests
import os
from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import send_from_directory
from werkzeug import secure_filename
from hashlib import md5

import pandas as pd

from config import *
from scoring import get_scores, plot_scores

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'tsv'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    kwargs = {'logins':LOGINS}

    if request.method == 'POST':
        file = request.files['file']
        team = request.form['team']
        kwargs['team'] = team
        pwd = request.form['pwd']
        if md5(SALT+team+pwd).hexdigest() == LOGINS[team]:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fdir = os.path.join(app.config['UPLOAD_FOLDER'], team)
                if len(set(file.readline().split('\t')) & set(['collection_id', 'file_id', 'tag'])):
                    file.seek(0)
                    file.save(os.path.join(fdir, filename))
                    kwargs['uploaded']=filename
                else:
                    kwargs['error']='Je moet als kolommen collection_id, file_id en tag hebben'
            else:
                kwargs['error']='Je moet wel wat uploaden'
        else:
            kwargs['error']='Fout wachtwoord'

    try:
        scores = get_scores()
    except:
        kwargs['error']='parse error???'
    kwargs['plot'] = plot_scores(scores)
    kwargs['scores'] = scores


    return render_template('leaderboard.html', **kwargs)

if __name__ == '__main__':
    app.run(debug=True)