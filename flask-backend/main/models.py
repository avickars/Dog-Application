from main import db, ma

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password


# JSON Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','email','name','phone', 'password')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserSession(db.Model):
    __tablename__ = 'user_session'
    id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(80), unique=True, nullable=False)
    device_type = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer,
                          db.ForeignKey("user.id"), nullable=False,
                          index=True)

    def __init__(self, refresh_token, user_id, device_type):
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.device_type = device_type


# JSON Schema
class UserSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'refresh_token', 'user_id', 'device_type')


user_session_schema = UserSessionSchema()
user_session_s_schema = UserSessionSchema(many=True)

if __name__ == "__main__":
    print("conected to db")

