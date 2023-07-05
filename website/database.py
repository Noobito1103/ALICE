from . import db

class User(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    game_data = db.relationship('GameData', backref='user')
    profile_data = db.relationship('ProfileData', backref='user')
    feedback_data = db.relationship('Feedback', backref='user')
    
class GameData(db.Model):
    d_id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey(User._id))
    latScore = db.Column(db.Integer)
    addScore = db.Column(db.Integer)
    subScore = db.Column(db.Integer)
    mulScore = db.Column(db.Integer)
    divScore = db.Column(db.Integer)
    mixScore = db.Column(db.Integer)
    pastScore = db.Column(db.Integer)
    topScore = db.Column(db.Integer)
    totalScore = db.Column(db.Integer)
    rank = db.Column(db.String(50))

class ProfileData(db.Model):
    p_id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey(User._id))
    profilePic = db.Column(db.LargeBinary(length=(2**32) - 1))
    profileBio = db.Column(db.String(2000))
    bannerColor = db.Column(db.String(50))
    usernameColor = db.Column(db.String(50))
    bioColor = db.Column(db.String(50))
    gameColor = db.Column(db.String(50))
    
class Feedback(db.Model):
    f_id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.Integer, db.ForeignKey(User._id))
    subject = db.Column(db.String(100))
    description = db.Column(db.String(300))
