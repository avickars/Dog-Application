from main import db, ma

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def _init_(self, name, email, phone, password):
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

    def _init_(self, refresh_token, user_id, device_type):
        self.refresh_token = refresh_token
        self.user_id = user_id
        self.device_type = device_type


# JSON Schema
class UserSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'refresh_token', 'user_id', 'device_type')


user_session_schema = UserSessionSchema()
user_session_s_schema = UserSessionSchema(many=True)


class Pets(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                          db.ForeignKey("user.id"), nullable=False,
                          index=True)
    image_url = db.Column(db.String(80), nullable=False)
    breed= db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float)
    pet_name = db.Column(db.String)


    def _init_(self, user_id, image_url, breed, weight, height, pet_name):
        self.user_id = user_id
        self.image_url = image_url
        self.breed = breed
        self.weight = weight
        self.height = height
        self.pet_name = pet_name


# JSON Schema
class PetsSchema(ma.Schema):
    class Meta:
        fields = (
            'user_id', 'image_url', 'breed', 'weight', 'height', 'pet_name')

pets_schema = PetsSchema()
pets_s_schema = PetsSchema(many=True)


if __name__ == "_main_":
    print("conected to db")