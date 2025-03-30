from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from src.services.database import get_db, get_session, get_user_by_id

todo_bp = Blueprint('todo', __name__, url_prefix='/todo')

@todo_bp.route('/', methods=['GET'])
def todo_list():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid',"")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if not user:
        return redirect('/')

    cur.execute("SELECT id, task, completed, due_date FROM e_todos WHERE user_id = %s", (user_id,))
    todos = cur.fetchall()

    return render_template('after/index.html', current_user=user, todos=todos)

@todo_bp.route('/add', methods=['POST'])
def add_todo():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid',"")
    session = get_session(sessionid)

    if not session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    task = request.form.get('task')
    due_date = request.form.get('due_date')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    try:
        cur.execute("INSERT INTO e_todos (user_id, task, completed, due_date) VALUES (%s, %s, %s, %s)", (user_id, task, False, due_date))
        conn.commit()

        cur.execute("SELECT last_insert_id()")
        todo_id = cur.fetchone()[0]

        return jsonify({'id': todo_id, 'task': task, 'completed': False, 'due_date': due_date}), 201  # Trả về JSON

    except Exception as e:
        conn.rollback()
        print(f"Error adding todo: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@todo_bp.route('/complete/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id):
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid',"")
    session = get_session(sessionid)

    if not session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        cur.execute("UPDATE e_todos SET completed = TRUE WHERE id = %s AND user_id = %s", (todo_id, user_id))
        conn.commit()
        return jsonify({'success': True}), 200

    except Exception as e:
        conn.rollback()
        print(f"Error completing todo: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@todo_bp.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid',"")
    session = get_session(sessionid)

    if not session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        cur.execute("DELETE FROM e_todos WHERE id = %s AND user_id = %s", (todo_id, user_id))
        conn.commit()
        return jsonify({'success': True}), 200

    except Exception as e:
        conn.rollback()
        print(f"Error deleting todo: {e}")
        return jsonify({'error': 'Internal server error'}), 500
