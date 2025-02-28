import psycopg2

from src.models.session import Session
from src.models.user import User

conn = None
cur = None

def init_db(app):
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            database=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        cur = conn.cursor()
    except psycopg2.Error as e:
        exit()

def get_db():
    return conn, cur

def get_user(username):
    conn, cur = get_db()
    cur.execute("SELECT * FROM e_users WHERE username = %s", (username,))
    user_data = cur.fetchone()
    return User(user_data) if user_data else None

def get_session(sessionid):
    conn, cur = get_db()
    cur.execute("SELECT * FROM e_sessions WHERE sessionid = %s", (sessionid,))
    session_data = cur.fetchone()
    return Session(session_data) if session_data else None

def get_user_by_id(user_id):
    from src.models.user import User
    conn, cur = get_db()
    cur.execute("SELECT * FROM e_users WHERE user_id = %s", (user_id,))
    user_data = cur.fetchone()
    return User(user_data) if user_data else None