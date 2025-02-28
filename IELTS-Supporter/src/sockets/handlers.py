def init_socket_handlers(socketio):
    online_users = set()

    @socketio.on('new_user')
    def new_user(data):
        username = data.get("username")
        print(f"New user: {username}")
        socketio.emit('notify_new_user',
                      {'message': f'User {username} just registered!'},
                      broadcast=True)