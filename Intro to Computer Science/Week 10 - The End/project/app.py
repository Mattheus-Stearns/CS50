import os

# Importing key Libraries
from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask_session import Session
from datetime import datetime, timezone
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

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
        'scope': 'email profile',  # No 'openid'
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

@app.route("/")
@login_required
def index():
    user = session.get('user')
    return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        redirect_uri = url_for('auth_callback', _external=True)
        return google.authorize_redirect(redirect_uri)
    
    else:
        return render_template("login.html")
    

@app.route('/auth/callback')
def auth_callback():
    try:
        token = google.authorize_access_token()
        print("Token:", token)
        user_info = google.get('userinfo').json()
        print("User info:", user_info)
        session['user'] = user_info
        session['user_id'] = user_info['id']
        return redirect('/')
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Login failed: {e}"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')