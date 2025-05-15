from app import db

class Role(db.Model):
    __tablename__ = 'role'
    role = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', backref='role_ref', lazy=True)

class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(50), primary_key=True)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), db.ForeignKey('role.role'))

class RoleHierarchy(db.Model):
    __tablename__ = 'role_hierarchy'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), db.ForeignKey('role.role'))
    access = db.Column(db.String(50))
    ref_role = db.Column(db.String(50))
    ref_access = db.Column(db.String(50))

class Category(db.Model):
    __tablename__ = 'category'
    name = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    order = db.Column(db.Integer, name='`order`')  # Échappement du mot-clé réservé
    ref_name = db.Column(db.String(50))
    ref_parent = db.Column(db.String(50), db.ForeignKey('category.name'))
    parent = db.relationship('Category', remote_side=[name])

class Publication(db.Model):
    __tablename__ = 'publication'
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    on_line = db.Column(db.Boolean)
    priority = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    ref_author = db.Column(db.String(50), db.ForeignKey('user.email'))
    ref_category = db.Column(db.String(50), db.ForeignKey('category.name'))

class Photo(db.Model):
    __tablename__ = 'photo'
    path = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))

class PublicationPhoto(db.Model):
    __tablename__ = 'publication_photo'
    id = db.Column(db.Integer, primary_key=True)
    publication = db.Column(db.String(100), db.ForeignKey('publication.id'))
    photo = db.Column(db.String(50), db.ForeignKey('photo.path'))

class PublicationEvent(db.Model):
    __tablename__ = 'publication_event'
    id = db.Column(db.Integer, primary_key=True)
    publication = db.Column(db.String(100), db.ForeignKey('publication.id'))
    event = db.Column(db.String(100))
    date = db.Column(db.DateTime)

class HomePageContainer(db.Model):
    __tablename__ = 'home_page_container'
    name = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))
    order = db.Column(db.Integer, name='`order`')
    ref_name = db.Column(db.String(100))
    ref_publication = db.Column(db.String(100), db.ForeignKey('publication.id'))

class PublicationSchedule(db.Model):
    __tablename__ = 'publication_schedule'
    id = db.Column(db.Integer, primary_key=True)
    publication = db.Column(db.String(100), db.ForeignKey('publication.id'))
    day = db.Column(db.String(10))
    start = db.Column(db.Time)
    end = db.Column(db.Time)
    ref_day = db.Column(db.String(10))
    ref_email = db.Column(db.String(50), db.ForeignKey('user.email'))

class ScheduleTimes(db.Model):
    __tablename__ = 'schedule_times'
    day = db.Column(db.String(10), primary_key=True)
    start = db.Column(db.Time)
    end = db.Column(db.Time)

class PublicationContent(db.Model):
    __tablename__ = 'publication_content'
    publication = db.Column(db.String(100), db.ForeignKey('publication.id'), primary_key=True)
    lastname = db.Column(db.String(50), primary_key=True)
    firstname = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.String(100))

class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(50))