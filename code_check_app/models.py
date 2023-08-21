from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserFiles(models.Model):
    uploaded_by_user_id = models.IntegerField()
    file_name = models.TextField()
    upload_path = models.TextField()
    upload_date = models.DateTimeField(auto_now=True)
    change_date = models.DateTimeField(auto_now=True)
    new_file = models.BooleanField(default=True)
    check_result = models.TextField(default='Ожидает проверки')
    check_log = models.TextField(null=True)

    @property
    def converted_log(self):
        return self.check_log.replace('\'', '\"')

    @property
    def user(self) -> User:
        return User.objects.filter(id=self.uploaded_by_user_id)[0]


class UsersMail(models.Model):
    user_id = models.IntegerField()
    mail_send_date = models.DateTimeField()
    mail_theme = models.TextField()
    mail_message = models.TextField()

    @property
    def short_message(self):
        return self.mail_message[:150]

    @property
    def converted_message(self):
        return self.mail_message.replace('\'', '\"')
