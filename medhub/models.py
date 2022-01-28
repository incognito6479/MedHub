from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from medhub.choices import RESPONDER_GENDER


class Answer(models.Model):
	responder = models.ForeignKey('medhub.Responder', on_delete=models.PROTECT)
	poll = models.ForeignKey('medhub.Poll', on_delete=models.PROTECT)
	# question = models.ForeignKey('medhub.Question', on_delete=models.PROTECT)
	interrogator = models.ForeignKey('medhub.Interrogator', on_delete=models.PROTECT)
	main_answer = models.CharField(max_length=255)
	sub_answer = models.CharField(max_length=500, blank=True, null=True)

	def __str__(self):
		return f"{self.main_answer} | {self.responder_id}"


class Question(models.Model):
	main_question = models.CharField(max_length=500)
	sub_question = models.TextField(blank=True, null=True)

	def __str__(self):
		return f"{self.main_question}"


class Poll(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=255)
	questions = models.ManyToManyField('medhub.Question', related_name='poll_questions')

	def __str__(self):
		return f"{self.name}"


class Responder(models.Model):
	birth_date = models.CharField(max_length=255)
	gender = models.CharField(max_length=255)

	def __str__(self):
		return f"{self.gender} | {self.birth_date}"

	class Meta:
		verbose_name = "Oтветчики"
		verbose_name_plural = "Oтветчики"


class Interrogator(AbstractBaseUser):
	username = models.CharField(verbose_name='Username', max_length=255,unique=True)
	full_name = models.CharField(max_length=255, verbose_name="Полное имя")
	# responders = models.ManyToManyField('medhub.Responder', verbose_name="Oтветчики",
	# 									blank=True, null=True, related_name="interrogators_responder")

	USERNAME_FIELD = 'username'

	def __str__(self):
		return self.username

	def save(self):
		self.password = make_password(self.password)
		super().save()

	class Meta:
		verbose_name = "Oпрашивающий"
		verbose_name_plural = "Oпрашивающий"


class Token(models.Model):
	user = models.ForeignKey('medhub.Interrogator', on_delete=models.CASCADE)
	token = models.CharField(max_length=800)