# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django import forms
from weibovis.models import SystemUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SystemUserForm(forms.ModelForm):
    class Meta:
        model = SystemUser
        fields = ('rtype',)