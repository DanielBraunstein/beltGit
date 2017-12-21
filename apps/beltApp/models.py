# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
MONOMIAL_REGEX = re.compile(r'^[a-zA-Z0-9]\w+$')
BINOMIAL_REGEX = re.compile(r'^[a-zA-Z\.\+_-]{2,}[\ ]{1}[a-zA-Z0-9\.\+_-]{2,}$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        users = self.filter(email=post_data['email'])
        if users:
            user = users[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')
        if errors:
            return errors
        return user 

    def validate_registration(self, post_data):
        errors = []
        print "validating reg"
        # check all fields for emptyness
        if len(post_data['name']) < 4:
            errors.append("name field must be at least 4 characters")
            print "name error"
        # check name fields for letter characters            
        elif not re.match(BINOMIAL_REGEX, post_data['name']):
            errors.append('namesfields must contain only letter characters with the exception of a single space between first and last names')

        if len(post_data['alias']) < 2:
            errors.append("alias field must be at least 3 characters")
            print "alias error"
        # check alias fields for letter characters            
        elif not re.match(MONOMIAL_REGEX, post_data['alias']):
            errors.append('Alias fields must be composed solely of letter and number characters only')

        # check length of password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
         # check password == password_confirm
        elif post_data['password'] != post_data['confpassword']:
            errors.append("passwords do not match")

        #check bday
        if not post_data['birthday']:
            errors.append("birthday entry required")

        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
       
        if not errors:
            # check uniqueness of email
            if len(User.objects.filter(alias = post_data['alias'])) > 0:
                errors.append("alias already in use")
            elif len(User.objects.filter(email=post_data['email'])) > 0:
                errors.append("email already in use")
            else:
                hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
                print "preparing to make new user"
                new_user = self.create(
                    name=post_data['name'],
                    alias=post_data['alias'],
                    bday = post_data['birthday'],
                    email = post_data['email'],
                    password = hashed,
                )
                print "new user created"
                return new_user
        return errors

class User(models.Model):
    name = models.CharField(max_length=100) 
    alias = models.CharField(max_length = 50)
    #this assumes single-word aliases only, see manager
    friends = models.ManyToManyField('self', related_name = "friends")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    bday = models.DateField(default = "2000-01-01")
    objects = UserManager()
    def __str__(self):
        return "<User: {}>".format(self.name)

