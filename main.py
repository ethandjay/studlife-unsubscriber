from flask import Flask, render_template, request, redirect
from google.oauth2 import service_account
import googleapiclient.discovery
import json
import os

app = Flask(__name__)

sections = [
    ('All', 'all'),
    ('Cadenza', 'cadenza-staff'),
    ('Copy', 'copystaff'),
    ('Design', 'design-staff'),
    ('Forum', 'forumstaff'),
    ('News', 'newsstaff'),
    ('Night Note', 'staff'),
    ('Photo', 'photostaff'),
    ('Scene', 'scenestaff'),
    ('Sports', 'sportsstaff')
]

@app.route('/')
def hello_world():
    return render_template('index.html', sections=sections)

@app.route('/submit', methods=['POST'])
def submit():
    error = None
    if request.method == 'POST':
        
        section = request.form['section']
        email = request.form['email']
        
        SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.member', 'https://www.googleapis.com/auth/admin.directory.group']
        SERVICE_ACCOUNT_JSON = json.loads(os.environ['studlife-unsubscriber-cc008c44e4ba.json'])

        credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_JSON, scopes=SCOPES)
        delegated_credentials = credentials.with_subject('ethan.jaynes@studlife.com')
    
        admin = googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)

        if section == 'all':
            noneWorked = True
            for tup in sections[1:]:
                try:
                    admin.members().delete(groupKey=f'{top[1]}@studlife.com', memberKey=f'{email}').execute()
                except:
                    # Do nothing
                else:
                    noneWorked = False
                    alert = {'status':'success', 'message': f'{email} successfully unsubscribed from all sections'}
            if noneWorked:
                alert = {'status':'danger', 'message': f'Couldn\'t unsubscribe. Make sure you entered in your email correctly.'}                


        try:
            admin.members().delete(groupKey=f'{section}@studlife.com', memberKey=f'{email}').execute()
        except:
            alert = {'status':'danger', 'message': f'Couldn\'t unsubscribe. Make sure you selected the right section and entered in your email correctly.'}
        else:
            alert = {'status':'success', 'message': f'{email} successfully unsubscribed from {section}@studlife.com'}

    return render_template('index.html', sections=sections, alert=alert)

@app.errorhandler(404)
def page_not_found(e):

    return render_template('index.html', sections=sections)