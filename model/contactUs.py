from app import db
import datetime

class ContactUs(db.Model):
  __tablename__ = "contactUs" # Defining table name

  contactUsID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  emailID = db.Column(db.String(100))
  mobileNumber = db.Column(db.String(15))
  message = db.Column(db.Text)
  contactUsAddedOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  @classmethod
  def getContactUs():
    return ContactUs.query.all()

  def createContactUs(self):
    db.session.add(self)
    db.session.commit()
    db.session.flush()
    return self