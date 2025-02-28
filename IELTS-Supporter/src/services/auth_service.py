from flask import render_template, request, redirect, make_response, flash
from src.services.database import get_db, get_user
from src import bcrypt
import random


def login_user():
    conn, cur = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and bcrypt.check_password_hash(user.password, password):
            sessionid = str(random.randint(10 ** 10, 10 ** 20))
            cur.execute("INSERT INTO e_sessions (sessionid, user_id) VALUES (%s, %s)", (sessionid, user.id))
            conn.commit()
            resp = make_response(render_template('after/index.html', current_user=user))
            resp.set_cookie('sessionid', sessionid)
            return resp
        else:
            flash('Invalid username or password')
            return render_template('before/login.html')
    return None


def signup_user():
    conn, cur = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password cannot be empty')
            return redirect('/signup')

        if get_user(username):
            flash('Email is already exist')
            return redirect('/signup')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute(
            "INSERT INTO e_users (username, password, avatar, firstname, lastname, email, address, hobbies, job, skill) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (username, hashed_password, "default-avatar.png", "", "", "", "", "", "", "")
        )
        conn.commit()

        sessionid = str(random.randint(10 ** 10, 10 ** 20))
        user = get_user(username)
        cur.execute("INSERT INTO e_sessions (sessionid, user_id) VALUES (%s, %s)", (sessionid, user.id))
        conn.commit()
        resp = make_response(render_template('after/index.html', current_user=user))
        resp.set_cookie('sessionid', sessionid)
        return resp
    return None


def logout_user():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid', "")
    cur.execute("DELETE FROM e_sessions WHERE sessionid = %s", (sessionid,))
    conn.commit()
    return redirect('/')