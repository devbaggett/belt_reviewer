from __future__ import unicode_literals

from django.db import models
import re, bcrypt

class UserManager(models.Manager):
	def validateUser(self, postData):
		is_valid = True
		errors = []
		if len(postData.get('name')) < 2:
			errors.append('Name must not be blank')
			is_valid = False
		user = User.objects.filter(email=postData.get('email')).first()
		if user:
			errors.append('This email is already in use.')
			is_valid = False
		if not re.search(r'\w+\@\w+\.\w+', postData.get('email')):
			errors.append('You must provide a valid email.')
			is_valid = False
		if len(postData.get('password')) < 4:
			errors.append('Password must be greater than 4 characters')
			is_valid = False
		if postData.get('password') != postData.get('password_confirmation'):
			errors.append('Passwords do not match.')
			is_valid = False
		return {'status': is_valid, 'errors': errors}

	def createUser(self, postData):
		return User.objects.create(
			name 		= postData.get('name'),
			email		= postData.get('email'),
			password 	= bcrypt.hashpw(postData.get('password').encode(), bcrypt.gensalt()))

	def loginUser(self, postData):
		user = User.objects.filter(email=postData.get('email')).first()
		if user and bcrypt.checkpw(postData.get('password').encode(), user.password.encode()):
			return {'status': True, 'user': user}
		else:
			return {'status': False, 'message': 'Invalid Credentials'}

class ReviewManager(models.Manager):
	def validateBookAndReview(self, postData):
		is_valid = True
		errors = []
		if len(postData.get('title')) == 0:
			errors.append('Your title must not be blank')
			is_valid = False
		if len(postData.get('review')) == 0:
			errors.append('Your review must not be blank')
			is_valid = False
		if postData.get('rating') == '':
			errors.append('Your rating is invalid')
			is_valid = False
		elif int(postData.get('rating')) < 0 or int(postData.get('rating')) > 5:
			errors.append('Your rating is invalid')
			is_valid = False
		if 'list_author' not in postData and len(postData.get('new_author')) == 0:
			errors.append('You must select or create an author')
			is_valid = False
		if 'list_author' in postData and len(postData.get('new_author')) > 0:
			errors.append('Only one author may be selected')
			is_valid = False
		return {'status': is_valid, 'errors': errors}





class User(models.Model):
	name 		= models.CharField(max_length=255)
	email 		= models.CharField(max_length=255)
	password 	= models.CharField(max_length=255)
	created_at 	= models.DateField(auto_now_add=True)
	updated_at 	= models.DateField(auto_now=True)
	objects 	= UserManager()
	def __unicode__(self):
		return "ID: " + str(self.id) + "\nName: " + self.name

class Author(models.Model):
	name		= models.CharField(max_length=255)
	created_at 	= models.DateField(auto_now_add=True)
	updated_at 	= models.DateField(auto_now=True)
	def __unicode__(self):
		return "Author: " + self.name

class Book(models.Model):
	title		= models.CharField(max_length=255)
	# a book has one author, but an author can have many books
	author 		= models.ForeignKey(Author, related_name="books")
	created_at 	= models.DateField(auto_now_add=True)
	updated_at 	= models.DateField(auto_now=True)
	def __unicode__(self):
		return "Book: " + self.title

class Review(models.Model):
	review 		= models.TextField()
	rating		= models.IntegerField()
	# a review has one user, but a user can have many reviews
	user   		= models.ForeignKey(User, related_name="reviews")
	# a review has one book, but a book can have many reviews
	book  		= models.ForeignKey(Book, related_name="reviews")
	created_at 	= models.DateField(auto_now_add=True)
	updated_at 	= models.DateField(auto_now=True)
	objects		= ReviewManager()
	def __unicode__(self):
		return self.review