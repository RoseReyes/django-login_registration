from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def validate_register(self, postData):
        result ={'status': False
        }
        reg_error = []

        if len(postData['name']) < 1 or len(postData['alias']) < 1: 
            reg_error.append('Name and Alias is required')
        if len(postData['name']) < 2:
            reg_error.append('Name should be longer than 2 characters')
        if not EMAIL_REGEX.match(postData['email']):
            reg_error.append('Invalid email')

        # check database for duplicate email
        if len(User.objects.filter(email=postData['email'])) > 0:
            reg_error.append("This account is already in use. Log-in or use another email") 
        if len(postData['password']) < 8:
            reg_error.append('Password cannot be less than 8 characters')
        if postData['password'] != postData['cpassword']:
            reg_error.append('Passwords do not match')

        # IF the error list is empty then hashed the password and insert in the database
        if len(reg_error):
            result['errors'] = reg_error
        else:
            # hashed the password then add to the database - salt generation is already included in django's pwd hashing, encode() returns the
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt())
            new_user = User.objects.create(name = postData['name'], alias = postData['alias'], bday = postData['bday'], email = postData['email'],password = hashed)
            result['status'] = True
            result['user_id'] = new_user.id
        return result

    def validate_login(self, postData):
        error = []
        user = User.objects.filter(email=postData['email'])
        if len(user) > 0:
            hashed_password = user[0].password
            if not bcrypt.checkpw(postData['password'].encode(), hashed_password.encode()):
                error.append("Email not found")
        else:
            error.append("Email not found")
        if len(error):
            return error
        return user[0]

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bday = models.DateTimeField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __repr__(self):
        return "<name: {}, alias: {}, email: {}, bday: {}, created_at: {}".format(self.name, self.alias, self.email, self.bday,self.created_at)

class Post(models.Model):
    posted_by = models.ForeignKey(User, related_name = "uploaded_quotes") 
    quoted_by = models.CharField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=255)
    liked_by = models.ManyToManyField(User, related_name = "liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return "<posted_by: {}, message: {}, created_at: {}".format(self.posted_by,self.message, self.created_at)








