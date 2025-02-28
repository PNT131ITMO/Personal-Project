class User:
    def __init__(self, user_data):
        self.id = user_data[0]
        self.username = user_data[1]
        self.password = user_data[2]
        self.avatar = user_data[3]
        self.firstname = user_data[4]
        self.lastname = user_data[5]
        self.email = user_data[6]
        self.address = user_data[7]
        self.hobbies = user_data[8]
        self.job = user_data[9]
        self.skill = user_data[10]