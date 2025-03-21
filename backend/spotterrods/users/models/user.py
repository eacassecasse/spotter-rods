#!/usr/bin/python3
"""This module defines a class User"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.models import BaseModel


class UserRoles:
    DISPATCHER = 'dispatcher'
    DRIVER = 'driver'
    TECHNICIAN = 'technician'


ROLES = [
    (UserRoles.DISPATCHER, 'dispatcher'),
    (UserRoles.DRIVER, 'driver'),
    (UserRoles.TECHNICIAN, 'technician'),
    ]


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username address must not be empty')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """This class defines a user by various attributes"""
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(choices=ROLES, default='driver', max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'password']

    class Meta:
        db_table = 'users'
