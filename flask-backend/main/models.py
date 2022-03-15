from main import db, ma

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fcm_token = db.Column(db.String(300), nullable=False)

    def _init_(self, email, password, fcm_token):
        self.email = email
        self.password = password
        self.fcm_token = fcm_token


# JSON Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','email', 'fcm_token')

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
    is_lost = db.Column(db.Integer)
    dog_extractor = db.Column(db.JSON)
    dog_identification = db.Column(db.JSON)
    final_output= db.Column(db.JSON)


    def _init_(self, user_id, image_url, is_lost, dog_extractor, dog_identification, final_output):
        self.user_id = user_id
        self.image_url = image_url
        self.is_lost = is_lost
        self.dog_extractor = dog_extractor
        self.dog_identification = dog_identification
        self.final_output = final_output


# JSON Schema
class PetsSchema(ma.Schema):
    class Meta:
        fields = (
            'user_id', 'image_url', 'is_lost', 'final_output')


# JSON Schema
class PetsSchemaUp(ma.Schema):
    class Meta:
        fields = (
            'id', 'image_url', 'dog_identification')

pets_schema = PetsSchema()
pets_s_schema = PetsSchema(many=True)
pets_up_schema = PetsSchemaUp(many=True)


if __name__ == "_main_":
    print("conected to db")