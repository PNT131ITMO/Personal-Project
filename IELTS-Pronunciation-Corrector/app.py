import random
import os

import psycopg2
from flask import Flask, render_template, request, redirect, make_response, flash, jsonify
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")

DB_HOST = 'localhost'
DB_PORT = 5656
DB_NAME = 'studs'
DB_USER = 's374807'
DB_PASSWORD = '9cs4jxVhIg4Vqi8D'

conn = None
cur = None
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
except psycopg2.Error as e:
    exit()

online_users = set()

def get_user(username):
    cur.execute("SELECT * FROM e_users WHERE username = %s", (username,))
    user = cur.fetchone()
    return user

def get_session(sessionid):
    cur.execute("SELECT * FROM e_sessions WHERE sessionid = %s", (sessionid,))
    session = cur.fetchone()
    return session
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        sessionid = request.cookies.get('sessionid', "")
        session = get_session(sessionid)
        
        if session is not None:
            return render_template('index.html')
        else:
            return render_template('index.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        
        if user and bcrypt.check_password_hash(user[2], password):
            sessionid = str(random.randint(10**10, 10**20))
            cur.execute("INSERT INTO e_sessions (sessionid, user_id) VALUES (%s, %s)", (sessionid, user[0]))
            conn.commit()
            resp = make_response(redirect('/profile'))
            resp.set_cookie('sessionid', sessionid)
            return resp
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password cannot be empty')
            return redirect('/signup')

        user = get_user(username)
        if user:
            flash('Email is already exist')
            return redirect('/signup')
        
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cur.execute(
                "INSERT INTO e_users (username, password, avatar, firstname, lastname, email, address, hobbies, job, skill) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (username, hashed_password, "default-avatar.png", "", "", "", "", "", "", "")
            )
            conn.commit()
            
            sessionid = str(random.randint(10**10, 10**20))
            user = get_user(username)
            cur.execute("INSERT INTO e_sessions (sessionid, user_id) VALUES (%s, %s)", (sessionid, user[0]))
            conn.commit()
            resp = make_response(redirect('/update-profile'))
            resp.set_cookie('sessionid', sessionid)
            return resp

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)
    if request.method == 'GET':
        if session is None:
            return redirect('/')
        else:
            user_id = session[1]
            cur.execute("SELECT * FROM e_users WHERE user_id = %s", (user_id,))
            user = cur.fetchone()

            username, firstname, lastname, avatar, email, address, hobbies, job, skill = (
                user[1], user[4], user[5], user[3], user[6], user[7], user[8], user[9], user[10]
            )
            return render_template('profile.html',
                                   username=username,
                                   firstname=firstname,
                                   lastname=lastname,
                                   avatar=avatar,
                                   email=email, address=address, hobbies=hobbies,
                                   job=job, skill=skill
                                   )
    
    if request.method == 'POST':
        username = session[1]

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cur.execute("UPDATE e_users SET firstname = %s, lastname = %s WHERE username = %s",
                    (firstname, lastname, username))
        conn.commit()
        resp = make_response(redirect('/profile'))
        return resp
    
        
@app.route('/logout')
def logout():
    sessionid = request.cookies.get('sessionid', "")
    cur.execute("DELETE FROM e_sessions WHERE sessionid = %s", (sessionid,))
    conn.commit()
    return redirect('/')


@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)
    if request.method == 'GET':
        if session:
            user_id = session[1]
            cur.execute("SELECT * FROM e_users WHERE user_id = %s", (user_id,))
            user = cur.fetchone()
            username, firstname, lastname, avatar, email, address, hobbies, job, skill = (
                user[1], user[4], user[5], user[3], user[6], user[7], user[8], user[9], user[10]
            )
            return render_template("update-profile.html",
                                   username=username,
                                   firstname=firstname,
                                   lastname=lastname,
                                   avatar=avatar,
                                   email=email, address=address, hobbies=hobbies,
                                   job=job, skill=skill
                                   )
        else:
            return redirect('/')
    else:
        user_id = session[1]

        new_firstname = request.form.get('firstname', '')
        new_lastname = request.form.get('lastname', '')
        new_email = request.form.get('email', '')
        new_address = request.form.get('address', '')
        new_hobbies = request.form.get('hobbies', '')
        new_job = request.form.get('job', '')
        new_skill = request.form.get('skill', '')

        update_fields = {}

        if new_firstname:
            update_fields['firstname'] = new_firstname
        if new_lastname:
            update_fields['lastname'] = new_lastname
        if new_email:
            update_fields['email'] = new_email
        if new_address:
            update_fields['address'] = new_address
        if new_hobbies:
            update_fields['hobbies'] = new_hobbies
        if new_job:
            update_fields['job'] = new_job
        if new_skill:
            update_fields['skill'] = new_skill

        if update_fields:
            sql = "UPDATE e_users SET "
            values = []
            for key, value in update_fields.items():
                sql += f"{key} = %s, "
                values.append(value)
            sql = sql[:-2]
            sql += " WHERE user_id = %s"
            values.append(user_id)
            cur.execute(sql, values)
            conn.commit()
        flash("Profile information update successfully")
        return redirect('/update-profile')

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if session:
        user_id = session[1]
        cur.execute("SELECT * FROM e_users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        username, firstname, lastname, avatar, job = (
            user[1], user[4], user[5], user[3], user[9]
        )
        if request.method == "GET":
            return render_template("pass_change.html",
                                   username=username,
                                   firstname=firstname,
                                   lastname=lastname,
                                   avatar=avatar,
                                   job=job
                                   )
        else:
            password, new_password, replay_new_pass = (
                request.form[key] for key in ["password", "new-password", "replay-new-pass"]
            )
            old_password = user[2]
            if bcrypt.check_password_hash(old_password, password):
                if new_password == replay_new_pass:
                    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                    cur.execute("UPDATE e_users SET password = %s WHERE user_id = %s", (hashed_password, user_id))
                    conn.commit()
                    flash("Change password successfully")
                    return redirect('/change-password')
                
                else:
                    flash("Password confirmation doesn't match")
                    return redirect('/change-password')
            else:
                flash("Old password isn't correct")
                return redirect('/change-password')
    else:
        return redirect('/')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-image', methods=['POST'])
def upload_image():
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)
    user_id = session[1]
    if request.method == 'POST':
        image = request.files['image']    
        if not image:
            flash("No file part")
            return redirect('/profile')
        if not image.filename:
            flash("No selected file")
            return redirect('/profile') 
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("UPDATE e_users SET avatar = %s WHERE user_id = %s", (filename, user_id))
            conn.commit()
            flash("Image uploaded successfully")
            return redirect('/profile')
@app.route('/')
def home():


@socketio.on('new_user')
def new_user(data):
    username = data.get("username")
    print(f"New user: {username}")

    emit('notify_new_user', {'message': f'User {username} just registered!'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    app.run(host='localhost', port=5000, debug=True)