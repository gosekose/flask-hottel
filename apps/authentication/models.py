from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, Float, TEXT

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    userId = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(64), nullable=False, unique=True) 
    password = Column(LargeBinary, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    phoneNumber = Column(String(64), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():

            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass(value)
            setattr(self, property, value)

    def __repr__(self):
        self.info = {
            "userId": self.userId,
            "userName": self.userName,
            "email": self.email,
            "phoneNumber": self.phoneNumber
        }
        return str(self.info)


class BusinessRegisters(db.Model):

    __tablename__ = "BusinessRegisters"

    businessRegisId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    businessNumber = Column(String(200), unique=True, nullable=False)
    users = db.relationship('Users', backref='BusinessRegisters')

    def __repr__(self):
        self.info = {
            "businessRegisId": self.businessRegisId,
            "userId": self.userId,
            "businessNumber": self.businessNumber
        }
        return str(self.info)


class BusinessLists(db.Model):

    __tablename__ = "BusinessLists"

    businessId = Column(Integer, primary_key=True)
    businessAddr = Column(String(200), nullable=False, unique=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    user = db.relationship('Users', backref='BusinessLists')

    def __repr__(self):
        self.info = {
            "businessId": self.businessId,
            "businessAddr": self.businessAddr,
            "userId": self.userId
        }
        return str(self.info)

class Accomodations(db.Model):

    __tablename__ = "Accomodations"

    accomodationId = Column(Integer, ForeignKey('BusinessLists.businessId'), primary_key=True)
    accomodationType = Column(String(100), nullable=False)
    accomodationName = Column(String(100), nullable=False)
    accomodationImage = Column(String(300))
    accomodationPrice = Column(String(200))

    businessLists = db.relationship('BusinessLists', backref='Accomodations')

    def __repr__(self):
        self.info = {
            "accomodationId": self.accomodationId,
            "accomodationType": self.accomodationType,
            "accomodationName": self.accomodationName,
            "accomodationImage": self.accomodationImage,
            "accomodationPrice": self.accomodationPrice,
        }
        return str(self.info)
   
class Rooms(db.Model):

    __tablename__ = 'Rooms'

    roomId = Column(Integer, primary_key=True, autoincrement=True)
    roomDateTime = Column(DateTime, nullable=False)
    roomNumber = Column(Integer, nullable=False)
    roomName = Column(String(200), nullable=False)
    roomCheckIn = Column(DateTime, nullable=False)
    roomCheckOut = Column(DateTime, nullable=False)
    roomStandardPopulation =Column(Integer)
    roomUptoPopulation =Column(Integer)
    roomImage = Column(String(300))
    roomSalePrice = Column(String(100), nullable=True)
    roomOriginalPrice = Column(String(100))
    roomRate = Column(Float, nullable=True)
    accomodationId = Column(Integer, ForeignKey('Accomodations.accomodationId'))

    accomodations = db.relationship('Accomodations', backref='Rooms')

    def __repr__(self):
        self.info = {
            "roomId": self.roomId,
            "roomDateTime": self.roomDateTime,
            "roomNumber": self.roomNumber,
            "roomName": self.roomName,
            "romeCheckIn": self.roomCheckIn,
            "romeCheckOut": self.roomCheckOut,
            "roomStandardPopulation": self.roomStandardPopulation,
            "roomUptoPopulation": self.roomUptoPopulation,
            "romeImage": self.roomImage,
            "roomSalePrice": self.roomSalePrice,
            "romeOriginalPrice": self.roomOriginalPrice,
            "roomRate": self.roomRate,
            "accomodationId": self.accomodationId
        }
        return str(self.info) 

class Carts(db.Model):

    __tablename__ = 'Carts'

    cartId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    roomId = Column(Integer, ForeignKey('Rooms.roomId'))

    users = db.relationship('Users', backref='Carts')
    rooms = db.relationship('Rooms', backref='Carts')

    def __repr__(self):
        self.info = {
            "cartId": self.cartId,
            "userId": self.userId,
            "roomId": self.roomId
        }
        return str(self.info)
    
class Reservations(db.Model):
    
    __tablename__ = 'Reservations'

    reserveId = Column(Integer, primary_key=True, autoincrement=True)
    reserveTime = Column(DateTime, nullable=False)
    reservePrice = Column(String(200), nullable=False)
    cartId = Column(Integer, ForeignKey('Carts.cartId'))

    carts = db.relationship('Carts', backref='Reservations')

    def __repr__(self):
        self.info = {
            "reserveId": self.reserveId,
            "reserveTime": self.reserveTime,
            "reservePrice": self.reservePrice,
            "cartId": self.cartId
        }
        return str(self.info) 


class Testimonials(db.Model):

    __tablename__ = 'Testimonials'

    testimonialId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    testimonialComment = Column(String(1000), nullable=False)

    users = db.relationship('Users', backref='Testimonials')

    def __repr__(self):
        self.info = {
            "testimonialId": self.testimonialId,
            "userId": self.userId,
            "testimonialComment": self.testimonialComment,
        }
        return str(self.info) 


class Reviews(db.Model):
    
    __tablename__ = 'Reviews'

    reviewId = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, ForeignKey('Users.userId'))
    reviewImage1 = Column(String(400), nullable=True)
    reviewImage2 = Column(String(400), nullable=True)
    reviewImage3 = Column(String(400), nullable=True)
    reviewComment = Column(String(1000), nullable=False)

    users = db.relationship('Users', backref='Reviews')

    def __repr__(self):
        self.info = {
            "reviewId": self.reviewId,
            "userId": self.userId,
            "reviewImage1": self.reviewImage1,
            "reviewImage2": self.reviewImage2,
            "reviewImage3": self.reviewImage3,
            "reviewComment": self.reviewComment,
        }
        return str(self.info) 

class Points(db.Model):

    __tablename__ = 'Points'

    userId = Column(Integer, ForeignKey('Users.userId'), primary_key=True)
    pointSum = Column(Integer)

    users = db.relationship('Users', backref='Points')

    def __repr__(self):
        self.info = {
            "userId": self.userId,
            "pointSum": self.pointSum,
        }
        return str(self.info) 

class Magazines(db.Model):

    __tablename__ = 'Magazines'

    magazineSeq = Column(Integer, primary_key=True, autoincrement=True)
    magazineId = Column(Integer, ForeignKey('Users.userId'))
    magazineThema = Column(String(200), nullable=False)
    magazineWriter = Column(String(400), nullable=False)
    magazineDate = Column(DateTime, nullable=False)
    magazineView = Column(Integer, nullable=False)
    magazineTitle = Column(String(400), nullable=False)
    magazineSubTitle = Column(String(400), nullable=True)
    magazineContent = Column(TEXT, nullable=False)
    magazineLink= Column(String(700), nullable=False)
    magazineTag= Column(String(800), nullable=False)
    magazineImage = Column(String(1000), nullable=True)

    users = db.relationship('Users', backref='Magazines')

    def __repr__(self):
        self.info = {
            "magazineSeq": self.magazineSeq,
            "magazineId": self.magazineId,
            "magazineThema": self.magazineThema,
            "magazineWriter": self.magazineWriter,
            "magazineDate": self.magazineDate,
            "magazineView": self.magazineView,
            "magazineTitle": self.magazineTitle,
            "magazineSubTitle": self.magazineSubTitle,
            "magazineContent": self.magazineContent,
            "magazineLink": self.magazineLink,
            "magazineTag": self.magazineTag,
            "magazineImage": self.magazineImage
        }

        return str(self.info) 


@login_manager.user_loader
def user_loader(userId):
    return Users.query.filter_by(useId=userId).first()


@login_manager.request_loader
def request_loader(request):
    userName = request.form.get('userName')
    user = Users.query.filter_by(userName=userName).first()
    return user if user else None