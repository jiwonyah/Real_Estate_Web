import os

BASE_DIR = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'minyong.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

