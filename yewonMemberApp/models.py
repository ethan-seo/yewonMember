from __future__ import unicode_literals
from django.db import models
from phone_field import PhoneField
# import phonenumbers
# from test import numbers
# from phonenumbers import geo
import re

# Create your models here.
class CustomerManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        return errors
    
    def update_validator(self, reqPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST['name']) < 2:
            errors["name"] = "Name should be at least 2 characters"
        if len(reqPOST['password']) != 0:
            if len(reqPOST['password']) < 8:
                errors['password'] = "Passwords must be at least 8 characters"
            if reqPOST['password'] != reqPOST['password_conf']:
                errors['password_conf'] = "Passwords need to match"
        if not EMAIL_REGEX.match(reqPOST["email"]):
            errors['regex'] = "Email is not in correct format"
        return errors
    
    def login_validator(self, reqPOST):
        errors = {}
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST["phone_num"]) == 0 or len(reqPOST['password']) == 0:
            errors["req_fields"] = "All Fields are required"
        return errors


class Customer(models.Model):
    phone = PhoneField(E164_only=True,blank=True, help_text='Contact phone number')
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    password = models.TextField()
    points = models.IntegerField(default=0)
    newsletter_email = models.BooleanField(default=True)
    newsletter_text = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()

class NewsletterManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['title']) < 2:
            errors["title"] = "Title should be at least 2 characters"
        if len(reqPOST['content']) < 5:
            errors["content"] = "Content should be at least 5 characters"
        return errors

class Newsletter(models.Model):
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = NewsletterManager()