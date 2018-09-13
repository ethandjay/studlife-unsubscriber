from flask import Flask, render_template, request, redirect
from google.oauth2 import service_account
import googleapiclient.discovery
import json

app = Flask(__name__)

sections = [
    ('Cadenza', 'cadenza-staff'),
    ('Copy', 'copystaff'),
    ('Design', 'design-staff'),
    ('Forum', 'forumstaff'),
    ('News', 'newsstaff'),
    ('Online', 'online'),
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
        SERVICE_ACCOUNT_JSON = json.loads(ENV['studlife-unsubscriber-cc008c44e4ba.json'])

        credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_JSON, scopes=SCOPES)
        delegated_credentials = credentials.with_subject('ethan.jaynes@studlife.com')
    
        admin = googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)

        try:
            admin.members().delete(groupKey=f'{section}@studlife.com', memberKey=f'{email}').execute()
        except:
            alert = {'status':'danger', 'message': f'Couldn\'t unsubscribe. Make sure you selected the right selection.'}
        else:
            alert = {'status':'success', 'message': f'{email} successfully unsubscribed from {section}@studlife.com'}

    return render_template('index.html', sections=sections, alert=alert)

@app.errorhandler(404)
def page_not_found(e):

    return render_template('index.html', sections=sections)