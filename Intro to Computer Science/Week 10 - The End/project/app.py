import os

# Importing key Libraries
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
from functools import wraps
from flask_session import Session
from datetime import datetime, timezone
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Configure application
app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={
        'scope': 'email profile https://www.googleapis.com/auth/documents'
    }
)

# Decorate routes to require login.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Adds context (who is the user?) to each page
@app.context_processor
def inject_user():
    return dict(user=session.get('user'))

# This is the Homepage
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Defining URL Patterns
DOCS_URL_PATTERN = re.compile(r"^https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)/edit(\?.*)?$")

# Login Process, calling google's redirect uri
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        redirect_uri = url_for('auth_callback', _external=True)
        return google.authorize_redirect(redirect_uri)
    
    else:
        return render_template("login.html")

# Ensuring that the user gets authenticated
@app.route("/auth/callback")
def auth_callback():
    try:
        token = google.authorize_access_token()
        session['credentials'] = {
        'token': token['access_token'],
        'refresh_token': token.get('refresh_token'),
        'token_uri': 'https://oauth2.googleapis.com/token',
        'client_id': os.getenv("GOOGLE_CLIENT_ID"),
        'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),
        'scopes': ['https://www.googleapis.com/auth/documents']
        }
        print("Token:", token)
        user_info = google.get('userinfo').json()
        print("User info:", user_info)
        session['user'] = user_info
        session['user_id'] = user_info['id']
        session['token'] = token
        return redirect('/')
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Login failed: {e}"

# Logout process
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# Docs Automation Implementation
@app.route("/docs", methods=["GET", "POST"])
@login_required
def docs():
    if request.method == "POST":
        errors = {}
        link = request.form.get("link")
        text_to_insert = request.form.get("text")

        if not link:
            errors["link"] = "Link is required."
        elif not DOCS_URL_PATTERN.match(link):
            errors["link"] = "Invalid Google Docs link format."
        
        if not text_to_insert.strip():
            errors["text"] = "Text to insert is required."

        if errors:
            return render_template("docs.html", errors=errors, values=request.form)
        
        document_id = DOCS_URL_PATTERN.match(link).group(1)
        creds_data = session.get('credentials')

        if not creds_data:
            return "User not authenticated.", 401

        creds = Credentials(**creds_data)
        docs_service = build('docs', 'v1', credentials=creds)
        doc = docs_service.documents().get(documentId=document_id).execute()
        end_index = doc.get('body').get('content')[-1]['endIndex']

        requests = [
            {
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': f"\n{text_to_insert}"
                }
            }
        ]

        try:
            result = docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
            return redirect("/")
        except Exception as e:
            errors['api'] = f"Failed to insert text: {e}"
            return render_template("docs.html", errors=errors, values=request.form)

    else:
        return render_template("docs.html", errors={}, values={})