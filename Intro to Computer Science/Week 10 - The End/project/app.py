import os

# Importing key Libraries
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
from functools import wraps
from flask_session import Session
from datetime import datetime, timezone, timedelta
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email_validator import validate_email, EmailNotValidError
import base64
from email.mime.text import MIMEText
import pytz
import urllib.parse

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
        'scope': (
            'email profile '
            'https://www.googleapis.com/auth/documents '
            'https://www.googleapis.com/auth/gmail.send '
            'https://www.googleapis.com/auth/calendar.events '
            'https://www.googleapis.com/auth/spreadsheets '
            'https://www.googleapis.com/auth/drive.readonly '
            'https://www.googleapis.com/auth/forms '
            'https://www.googleapis.com/auth/forms.responses.readonly'
        )
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

# Defining Patterns
DOCS_URL_PATTERN = re.compile(r"^https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)/edit(.*)?$")
SHEETS_URL_PATTERN = re.compile(r"^https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)/edit(.*)?$")
FORMS_URL_PATTERN = re.compile(r"^https://docs\.google\.com/forms/d/([a-zA-Z0-9_-]+)/edit(.*)?$")
CELL_PATTERN = re.compile(r"^[A-Za-z]{1,3}[1-9][0-9]*$")

# Normalizing URLs
def normalize_url(url, pattern):
    match = pattern.match(url)
    if not match:
        return None
    
    file_id = match.group(1)
    idx = url.find(file_id)
    if idx == -1:
        return None

    return url[:idx] + file_id + "/edit"

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
            'scopes': [
                'https://www.googleapis.com/auth/documents',
                'https://www.googleapis.com/auth/gmail.send',
                'https://www.googleapis.com/auth/calendar.events',
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.readonly',
                'https://www.googleapis.com/auth/forms',
                'https://www.googleapis.com/auth/forms.responses.readonly'
            ]
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

# Mail Automation Implementation
@app.route("/mail", methods=["GET", "POST"])
@login_required
def mail():
    if request.method == "POST":
        errors = {}
        destination = request.form.get("destination")
        copy = request.form.get("copy")
        subject = request.form.get("subject")
        text = request.form.get("text")

        if not destination:
            errors["destination"] = "Destination is required."
        if not subject:
            errors["subject"] = "Subject is required."
        if not text:
            errors["text"] = "Message text is required."

        # These only check if the addresses are in the correct format, to check if the adresses exist you need a paid api
        try:
            destination = validate_email(destination).email
        except EmailNotValidError as e:
            errors["destination"] = str(e)

        if copy:
            try:
                copy = validate_email(copy).email
            except EmailNotValidError as e:
                errors["copy"] = str(e)
        
        if errors:
            return render_template("mail.html", errors=errors, values=request.form.copy())
        
        creds_data = session.get('credentials')
        if not creds_data:
            return "Authentication credentials not found. Please log in again.", 401

        creds = Credentials(**creds_data)
        mail_service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(text)
        message['to'] = destination
        if copy:
            message['cc'] = copy
        message['from'] = session['user']['email']
        message['subject'] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            send_result = mail_service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
        except Exception as e:
            errors['send_error'] = f"Failed to send email: {e}"
            return render_template("mail.hmtl", errors=errors, values=request.form.copy())

        mail_url = f'https://mail.google.com/mail/?authuser={session["user"]["email"]}#sent'
        return render_template("mail.html", redirect_url=mail_url, back_url="/", errors={}, values={})
    
    else:
        return render_template("mail.html", errors={}, values={})
    
# Calendar Automation Implementation
@app.route("/calendar", methods=["GET", "POST"])
@login_required
def calendar():
    if request.method == "POST":
        errors = {}
        title = request.form.get("title")
        guest = request.form.get("guest")
        time = request.form.get("time")
        description = request.form.get("description")
        timezone = request.form.get("timezone", "UTC")

        if not title:
            errors["title"] = "Title is required."
        
        if not time:
            errors["time"] = "Time is required."

        if guest:
            try:
                guest = validate_email(guest).email
            except EmailNotValidError as e:
                errors["guest"] = str(e)
        
        try:
            dt = datetime.strptime(time, "%Y-%m-%dT%H:%M")
        except (ValueError, TypeError):
            errors["time"] = "Please enter a valid date and time."
        
        if dt < datetime.now():
            errors["time"] = "Please select a future date and time."

        if timezone not in pytz.all_timezones:
            timezone = "UTC"

        if errors:
            return render_template("calendar.html", errors=errors, values=request.form.copy())
        
        creds_data = session.get('credentials')
        if not creds_data:
            return "Authentication credentials not found. Please log in again.", 401
        
        creds = Credentials(**creds_data)
        calendar_service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': dt.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': (dt + timedelta(hours=1)).isoformat(),
                'timeZone': timezone,
            },
        }

        if guest:
            event['attendees'] = [{'email': guest}]

        try:
            created_event = calendar_service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
            redirect_url = created_event.get("htmlLink")
            flash("Event successfully created in Google Calendar!", "success")
        except Exception as e:
            errors["api"] = f"Failed to create event: {e}"
            return render_template("calendar.html", errors=errors, values=request.form.copy())
        
        redirect_url = f'{redirect_url}&authuser={session["user"]["email"]}'
        return render_template("calendar.html", redirect_url=redirect_url, back_url="/", errors={}, values={})

    else:
        return render_template("calendar.html", errors={}, values={})

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
        if not DOCS_URL_PATTERN.match(link):
            errors["link"] = "Invalid Google Docs link format."
        
        if not text_to_insert.strip():
            errors["text"] = "Text to insert is required."

        if errors:
            return render_template("docs.html", errors=errors, values=request.form.copy())
        
        document_id = DOCS_URL_PATTERN.match(link).group(1)
        link = normalize_url(link, DOCS_URL_PATTERN)
        creds_data = session.get('credentials')

        if not creds_data:
            return "Authentication credentials not found. Please log in again.", 401

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
        except Exception as e:
            errors['api'] = f"Failed to insert text: {e}"
            return render_template("docs.html", errors=errors, values=request.form())

        return render_template("docs.html", redirect_url=link, back_url="/", errors={}, values={})

    else:
        return render_template("docs.html", errors={}, values={})
    
# Sheets Automation Implementation
@app.route("/sheets", methods=["GET", "POST"])
@login_required
def sheets():
    if request.method == "POST":
        errors = {}
        link = request.form.get("link")
        cell = request.form.get("cell")
        text = request.form.get("text")

        if not link:
            errors["link"] = "Link is required."
        if not SHEETS_URL_PATTERN.match(link):
            errors["link"] = "Invalid Google Sheets link format."
        
        if not cell:
            errors["cell"] = "Cell is required."
        if not CELL_PATTERN.match(cell):
            errors["cell"] = "Invalid cell format."
        
        if not text.strip():
            errors["text"] = "Text to insert is required."

        if errors:
            return render_template("sheets.html", errors=errors, values=request.form.copy())
        
        sheet_id = SHEETS_URL_PATTERN.match(link).group(1)
        link = normalize_url(link, SHEETS_URL_PATTERN)
        creds_data = session.get('credentials')

        if not creds_data:
            return "Authentication credentials not found. Please log in again.", 401
        
        creds = Credentials(**creds_data)
        service = build('sheets', 'v4', credentials=creds)

        try:
            response = service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=cell,
                valueInputOption="RAW",
                body={"values": [[text]]}
            ).execute()
        except Exception as e:
            errors["api"] = f"Failed to write to sheet: {e}"
            return render_template("sheets.html", errors=errors, values=request.form.copy())
        
        return render_template("sheets.html", redirect_url=link, back_url="/", errors={}, values={})
    else:
        return render_template("sheets.html", errors={}, values={})

# Forms Automation Implementation
@app.route("/forms", methods=["GET", "POST"])
@login_required
def forms():
    if request.method == "POST":
        errors = {}
        link = request.form.get("link")

        if not link:
            errors["link"] = "Link is required."
        else:
            match = FORMS_URL_PATTERN.match(link)
            if not match:
                errors["link"] = "Invalid Google Forms link format."

        if errors:
            return render_template("forms.html", errors=errors, values=request.form.copy())
        
        form_id = match.group(1)
        link = normalize_url(link, FORMS_URL_PATTERN)
        creds_data = session.get('credentials')

        if not creds_data:
            return "Authentication credentials not found. Please log in again.", 401
        
        creds = Credentials(**creds_data)

        try:
            forms_service = build('forms', 'v1', credentials=creds)
            response = forms_service.forms().responses().list(formId=form_id).execute()
            responses = response.get("responses", [])
        except Exception as e:
            errors["api"] = f"Failed to fetch responses: {e}"
            return render_template("forms.html", errors=errors, values=request.form.copy())

        return render_template("forms.html", responses=responses, values=request.form.copy(), errors={}, form_url=link)


    else:
        return render_template("forms.html", errors={}, values={})

# Search Automation Implementation
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        errors = {}
        query = request.form.get("query")
        action = request.form.get("action")

        if not query:
            errors["query"] = "Search is required."

        if errors:
            return render_template("forms.html", errors=errors, values=request.form.copy())
        
        encoded_query = urllib.parse.quote_plus(query)

        if action == "search":
            url = f"https://www.google.com/search?q={encoded_query}"
        elif action == "lucky":
            url = f"https://www.google.com/search?q={encoded_query}&btnI=I"        

        return render_template("sheets.html", redirect_url=url, back_url="/", errors={}, values={})
        
    else:
        return render_template("search.html", errors={}, values={})