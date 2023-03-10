from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(
        self, first_name, last_name, phone_number, username, email, password=None
    ):
        if not email:
            raise ValueError("User must have email address")

        if not username:
            raise ValueError("User must have username")

        user = self.model(
            email=self.normalize_email(
                email
            ),  # If user enter CAP email, it will convert to small case.
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, phone_number, username, email, password
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(
        max_length=20,
    )
    last_name = models.CharField(
        max_length=20,
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=25)

    # Required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "phone_number"]

    objects = MyAccountManager()

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class AccountProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line1 = models.CharField(blank=True, max_length=100)
    address_line2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to="account_profile")
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)

    def __str__(self) -> str:
        return str(self.user.email)

    def full_address(self):
        return f"{self.address_line1}, {self.address_line2}"
