from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(
        self, username, email, password, name, nickname, birth_date, **extra_fields
    ):
        if not username:
            raise ValueError("The Username field is required.")
        if not email:
            raise ValueError("The Email field is required.")
        if not password:
            raise ValueError("The Password field is required.")
        if not name:
            raise ValueError("The Name field is required.")
        if not nickname:
            raise ValueError("The Nickname field is required.")
        if not birth_date:
            raise ValueError("The Birth Date field is required.")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            name=name,
            nickname=nickname,
            birth_date=birth_date,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, email, password, name, nickname, birth_date, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            username, email, password, name, nickname, birth_date, **extra_fields
        )


class Account(AbstractBaseUser):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=30)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    bio = models.TextField(blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name", "nickname", "birth_date"]

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.username
