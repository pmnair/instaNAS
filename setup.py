
import pymongo
import hashlib
import bcrypt
from setuptools import setup

setup(name='instaNAS',
        version='1.0',
        description='Simple NAS Application Server',
        author='Praveen M Nair',
        author_email='praveen.nair@icloud.com',
        url='http://www.python.org/sigs/distutils-sig/',
        install_requires=['tornado','pymongo','py-bcrypt'],
        )

dbconn = pymongo.MongoClient('mongodb://localhost:27017/')
db = dbconn['insta-nas-db']['admins']
admin = db.find_one({'user': 'admin'})
if admin:
    db.remove({'user': 'admin'})

phash = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt(8))
u = {}
u['user'] = 'admin'
u['password'] = phash
u['secret'] = hashlib.sha1('admin/%s' % (phash)).hexdigest()
db.save(u)

