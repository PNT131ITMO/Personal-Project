from flask import Blueprint, render_template, request
from src.services.database import get_session, get_user_by_id
from src.services.auth_service import login_user, signup_user, logout_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if request.method == 'GET':
        print(f"Session ID: {sessionid}, Session: {session.__dict__ if session else 'None'}")
        if session and hasattr(session, 'user_id'):
            user = get_user_by_id(session.user_id)
            return render_template('after/index.html', current_user=user)
        return render_template('before/index.html')

    result = login_user()
    return result if result else render_template('before/login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if request.method == 'GET':
        if session:
            user = get_user_by_id(session.user_id)
            return render_template('after/index.html', current_user=user)
        return render_template('before/login.html')

    result = login_user()
    if result:
        return result
    return render_template('before/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('before/signup.html')
    return signup_user()

@auth_bp.route('/logout')
def logout():
    return logout_user()