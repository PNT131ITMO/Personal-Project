from flask import Blueprint, render_template, request, redirect, flash

from src.models.user import User
from src.services.database import get_db, get_session, get_user
from src import bcrypt
from src.utils.file_utils import allowed_file
from werkzeug.utils import secure_filename
import os

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET', 'POST'])
def profile():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if request.method == 'GET':
        return render_template('after/profile.html',
                               username=user.username,
                               firstname=user.firstname,
                               lastname=user.lastname,
                               avatar=user.avatar,
                               email=user.email,
                               address=user.address,
                               hobbies=user.hobbies,
                               job=user.job,
                               skill=user.skill)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cur.execute("UPDATE e_users SET firstname = %s, lastname = %s WHERE user_id = %s",
                    (firstname, lastname, user_id))
        conn.commit()
        return redirect('/profile')


@profile_bp.route('/update', methods=['GET', 'POST'])
def update_profile():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if request.method == 'GET':
        return render_template('after/update-profile.html',
                               username=user.username,
                               firstname=user.firstname,
                               lastname=user.lastname,
                               avatar=user.avatar,
                               email=user.email,
                               address=user.address,
                               hobbies=user.hobbies,
                               job=user.job,
                               skill=user.skill)

    new_fields = {k: v for k, v in {
        'firstname': request.form.get('firstname', ''),
        'lastname': request.form.get('lastname', ''),
        'email': request.form.get('email', ''),
        'address': request.form.get('address', ''),
        'hobbies': request.form.get('hobbies', ''),
        'job': request.form.get('job', ''),
        'skill': request.form.get('skill', '')
    }.items() if v}

    if new_fields:
        sql = "UPDATE e_users SET " + ", ".join(f"{k} = %s" for k in new_fields) + " WHERE user_id = %s"
        cur.execute(sql, list(new_fields.values()) + [user_id])
        conn.commit()

    flash("Profile information updated successfully")
    return redirect('/profile/update')


@profile_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if request.method == 'GET':
        return render_template('after/pass_change.html',
                               username=user.username,
                               firstname=user.firstname,
                               lastname=user.lastname,
                               avatar=user.avatar,
                               job=user.job)

    password = request.form['password']
    new_password = request.form['new-password']
    replay_new_pass = request.form['replay-new-pass']

    if not bcrypt.check_password_hash(user.password, password):
        flash("Old password isn't correct")
        return redirect('/profile/change-password')

    if new_password != replay_new_pass:
        flash("Password confirmation doesn't match")
        return redirect('/profile/change-password')

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    cur.execute("UPDATE e_users SET password = %s WHERE user_id = %s", (hashed_password, user_id))
    conn.commit()
    flash("Change password successfully")
    return redirect('/profile/change-password')


@profile_bp.route('/upload-image', methods=['POST'])
def upload_image():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid', "")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    image = request.files['image']

    if not image or not image.filename:
        flash("No file selected")
        return redirect('/profile')

    if allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(profile_bp.root_path, '..', '..', 'static/images', filename))
        cur.execute("UPDATE e_users SET avatar = %s WHERE user_id = %s", (filename, user_id))
        conn.commit()
        flash("Image uploaded successfully")
    return redirect('/profile')


def get_user_by_id(user_id):
    conn, cur = get_db()
    cur.execute("SELECT * FROM e_users WHERE user_id = %s", (user_id,))
    user_data = cur.fetchone()
    return User(user_data) if user_data else None