from flask import Flask, render_template, request, redirect
from google.oauth2 import service_account
import googleapiclient.discovery

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/submit', methods=['POST'])
def submit():
    error = None
    if request.method == 'POST':
        SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.member', 'https://www.googleapis.com/auth/admin.directory.group']
        SERVICE_ACCOUNT_FILE = 'studlife-unsubscriber-cc008c44e4ba.json'

        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        delegated_credentials = credentials.with_subject('ethan.jaynes@studlife.com')
    
        admin = googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)
        ans = [o for o in dir(admin)]

    return str(admin.groups().get(groupKey='cadenza-staff@studlife.com').execute())
    # return str(ans)

@app.route('/oauth2callback')
def callback():
    return 'Called back'