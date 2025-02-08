from .app import db
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
import re


class AppInfo(db.Model):
    __tablename__ = 'appinfo'
    app_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    platform = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(255))
    download_link = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255))
    author = db.Column(db.String(255), nullable=False)

    @validates('app_id')
    def validate_id(self, key, app_id):
        print(app_id)
        # assert re.match(r'^[a-zA-Z0-9\.-_]+$', app_id)
        assert len(app_id.split('.')) == 2
        return app_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@event.listens_for(AppInfo, 'before_insert')
def generate_id(mapper, connection, target):
    # name_part = re.sub(r'\\s+', '-', target.name.lower())
    target.app_id = f"{target.author}.{target.name.lower().replace(' ', '-')}"

# class AppInfo(db.Model):
#     __tablename__ = 'AppInfo'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     app_link = db.Column(db.Text, nullable=False)
#     platform = db.Column(db.Text, nullable=False)
#     thumbnail = db.Column(db.Text, nullable=True)
#     version = db.Column(db.Text, nullable=False)
#     author = db.Column(db.Text, nullable=False)

#     def __repr__(self) -> str:
#         return f'<AppInfo {self.name} {self.version} {self.author}>'

#     def to_dict(self)-> dict:
#         return {
#                 'id': self.id,
#                 'name': self.name,
#                 'description': self.description,
#                 'app_link': self.app_link,
#                 'platform': self.platform,
#                 'thumbnail': self.thumbnail,
#                 'version': self.version,
#                 'author': self.author
#                 }
