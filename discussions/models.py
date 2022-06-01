from django.db import models
import uuid
from django.contrib.auth.models import User
from users.models import Profile
""" This module is where the database design of
    the web app 'discussions' implimented
"""



# Create your models here.
class Topic(models.Model):
	""" A class for topics since every discussion has a topic"""
	id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Room(models.Model):
	""" Every discussion happens inside a room of a specific topic"""
	id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
	host = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True) 
	topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank=True)
	participants = models.ManyToManyField(Profile, related_name='participants', blank= True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-updated', '-created']

	def __str__(self):
		return self.name

# Create your models here.
class Questions(models.Model):
	"""Inside Room we have quetions users can ask"""
	id = models.UUIDField( default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
	body = models.TextField()

	body_image = models.ImageField(null=True, blank=True, upload_to='questions/')

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-updated', '-created']

	def __str__(self):
		return self.body


class Answers(models.Model):
	"""  For Every question asked there are answers given """
	id = models.UUIDField( default=uuid.uuid4, unique=True, primary_key=True, editable=False)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	question = models.ForeignKey(Questions, on_delete=models.CASCADE)
	body = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-updated', '-created']

	def __str__(self):
		return self.body[0:50]