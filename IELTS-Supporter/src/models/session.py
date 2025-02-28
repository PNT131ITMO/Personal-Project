class Session:
    def __init__(self, session_data):
        if session_data:
            self.sessionid = session_data[0]
            self.user_id = session_data[1]
        else:
            self.sessionid = None
            self.user_id = None