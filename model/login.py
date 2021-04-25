from app import db
import datetime

class Login(db.Model):
  __tablename__ = "user" # Defining table name

  userID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  fullName = db.Column(db.String(100))
  emailID = db.Column(db.String(100))
  password = db.Column(db.String(200))
  userAddedOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  @classmethod
  def validateUser(self, emailID):
    return Login.query.filter_by(emailID = emailID).all()

  def createUser(self):
    db.session.add(self)
    db.session.commit()
    db.session.flush()
    return self