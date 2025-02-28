from flask import Blueprint, render_template, request, redirect, jsonify

from src.services.database import get_db, get_session, get_user_by_id

vocabulary_bp = Blueprint('vocabulary', __name__, url_prefix='/vocabulary')
@vocabulary_bp.route('/', methods=['GET', 'POST'])
def vocabulary():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid',"")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if not user:
        return redirect('/')

    cur.execute("SELECT deck_id, deck_name FROM e_decks WHERE user_id = %s", (user_id,))
    decks = cur.fetchall()

    if not decks:
        cur.execute("INSERT INTO e_decks (user_id, deck_name) VALUES (%s, 'Default') RETURNING deck_id, deck_name", (user_id,))
        default_deck = cur.fetchone()
        conn.commit()
        decks = [default_deck]
    selected_deck_id = request.args.get('deck_id', decks[0][0], type=int)

    if request.method == 'GET':
        cur.execute("SELECT card_id, front, back FROM e_cards WHERE deck_id = %s", (selected_deck_id,))
        vocabulary_items = cur.fetchall()

        return render_template('after/vocabulary.html',
                               vocabulary_items=vocabulary_items,
                               current_user=user,
                               decks=decks,
                               selected_deck_id=selected_deck_id)

    elif request.method == 'POST':
        front = request.form.get('front')
        back = request.form.get('back')
        deck_id = request.form.get('deck_id', selected_deck_id)

        if not front or not back:
            return redirect(f'/vocabulary/?deck_id={deck_id}')

        cur.execute('SELECT deck_id FROM e_decks WHERE deck_id = %s AND user_id = %s', (deck_id, user_id))
        deck = cur.fetchone()

        if not deck:
            return redirect(f'/vocabulary/?deck_id={selected_deck_id}')

        try:
            cur.execute('INSERT INTO e_cards (deck_id, front, back) VALUES (%s, %s, %s)', (deck_id, front, back))
            conn.commit()
        except Exception as e:
            conn.rollback()

        return redirect(f'/vocabulary/?deck_id={deck_id}')

    return render_template('after/vocabulary.html',
                           vocabulary_items=[],
                           current_user=user,
                           decks=decks,
                           selected_deck_id=selected_deck_id)

@vocabulary_bp.route('/create_deck', methods=['POST'])
def create_deck():
    conn, cur = get_db()
    sessionid = request.cookies.get('sessionid',"")
    session = get_session(sessionid)

    if not session:
        return redirect('/')

    user_id = session.user_id
    user = get_user_by_id(user_id)

    if not user:
        return redirect('/')

    deck_name = request.form.get('deck_name')

    if not deck_name:
        return redirect('/vocabulary/')

    try:
        cur.execute('INSERT INTO e_decks (user_id, deck_name) VALUES (%s, %s) RETURNING deck_id', (user_id, deck_name))
        new_deck_id = cur.fetchone()[0]
        conn.commit()
        return redirect(f'/vocabulary/?deck_id={new_deck_id}')
    except Exception as e:
        conn.rollback()
        return redirect('/vocabulary/')


@vocabulary_bp.route('/api/cards', methods=['GET'])
def get_cards():
    try:
        conn, cur = get_db()
        sessionid = request.cookies.get('sessionid', "")
        session = get_session(sessionid)

        if not session:
            return jsonify({'error': 'Unauthorized'}), 401

        user_id = session.user_id
        user = get_user_by_id(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404  # Trả về JSON thay vì redirect

        deck_id = request.args.get('deck_id', type=int)
        if not deck_id:
            return jsonify({'error': 'Missing or invalid deck_id parameter'}), 400

        cur.execute("""
            SELECT 1 FROM e_decks 
            WHERE deck_id = %s AND user_id = %s
        """, (deck_id, user_id))
        if not cur.fetchone():
            return jsonify({'error': 'Deck not found or access denied'}), 404

        cur.execute("""
            SELECT card_id, front, back 
            FROM e_cards 
            WHERE deck_id = %s
            ORDER BY card_id
        """, (deck_id,))

        cards = cur.fetchall()
        formatted_cards = [{
            'id': card[0],
            'front': card[1],
            'back': card[2]
        } for card in cards]

        return jsonify({'cards': formatted_cards})

    except Exception as e:
        print(f"Error fetching cards: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@vocabulary_bp.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
