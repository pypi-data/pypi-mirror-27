class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {username}>'

    def __str__(self):
        return f'<User {username}>'
