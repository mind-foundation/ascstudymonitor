"""
Stores the document library in a database
"""
# pylint: disable=missing-docstring,too-few-public-methods
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from ascmonitor import app
from ascmonitor.config import ascdb_uri
from ascmonitor.config import refresh_interval

last_refresh_key = 'LAST_REFRESH'

app.config['SQLALCHEMY_DATABASE_URI'] = ascdb_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable some bs warning

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Document(db.Model):
    id_ = db.Column(db.String(36), primary_key=True)
    bibliography = db.Column(db.JSON)


class CacheMeta(db.Model):
    key = db.Column(db.String(32), primary_key=True)

    # only one of these values should be set
    value = db.Column(db.String(32), nullable=True)
    datetime = db.Column(db.DateTime, nullable=True)


db.create_all()


def get_documents():
    """ Get the document store from the cache """
    return [doc.bibliography for doc in Document.query.all()]


def update_documents(documents):
    """ Update the library """
    # delete all
    Document.query.delete()

    # recreate from ground truth
    objects = [Document(id_=doc['id'], bibliography=doc) for doc in documents]
    db.session.bulk_save_objects(objects)

    _has_updated()

    db.session.commit()


def needs_update():
    """ Returns True if bibliography needs an update """
    last_refresh = CacheMeta.query.get(last_refresh_key)

    if last_refresh is not None:
        return last_refresh.datetime > datetime.now() + refresh_interval
    else:
        # flag doesnt exist yet
        return True


def _has_updated():
    """ Set last_refresh datetime to now """
    last_refresh = CacheMeta.query.get(last_refresh_key)
    if last_refresh is not None:
        last_refresh.datetime = datetime.now()
    else:
        last_refresh = CacheMeta(key=last_refresh_key, datetime=datetime.now())
        db.session.add(last_refresh)
        db.session.commit()
