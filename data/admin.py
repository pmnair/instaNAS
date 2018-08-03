#!/usr/bin/python

import os
import pymongo
import hashlib
import time
import bcrypt

class Admin(object):
    def __init__(self, db):
        self.db = db['admins']

    def exists(self, name):
        user = self.db.find_one({'user': name})
        if not user:
            raise Exception('User %s does not exist!' % name)
        return user

    def add(self, name, passwd):
        user = self.db.find_one({'user': name})
        if user:
            raise Exception("User '%s' already registered " % name)

        # Warning bcrypt will block IO loop:
        passwd_hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt(8))

        u = {}
        u['user'] = name
        u['password'] = passwd_hash
        u['secret'] = hashlib.sha1('%s/%s' % (name, passwd_hash)).hexdigest()
        if user:
            self.db.update({'user': name}, u)
        else:
            self.db.save(u)
        return u['secret']

    def check_password(self, name, passwd):
        user = self.exists(name)
        if bcrypt.hashpw(passwd.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:
            return True
        return False

    def check_secret(self, name, secret):
        user = self.exists(name)
        if user['secret'] and secret == user['secret']:
            return True
        return False

    def delete(self, name, passwd):
        user = self.exists(name)
        if bcrypt.hashpw(passwd.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:
            self.db.remove({'user': name})
        else:
            raise Exception("Password incorrect for '%s'!" % name)

    def update_password(self, name, passwd, new_passwd):
        user = self.exists(name)
        if bcrypt.hashpw(passwd.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:
            # Warning bcrypt will block IO loop:
            user['password'] = bcrypt.hashpw(new_passwd.encode('utf-8'), bcrypt.gensalt(8))
            self.db.update({'user': name}, user)
        else:
            raise Exception("Password incorrect for '%s'!" % name)


