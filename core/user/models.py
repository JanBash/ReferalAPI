from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)



class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        
        user = self.model(
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    
class Refer(models.Model):
    user = models.ForeignKey(
        'MyUser', 
        on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        'MyUser',
        related_name = 'Referers'
    )
    code = models.CharField(
        max_length = 50,
        unique = True
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    expire_date = models.DateField()
    is_expired = models.BooleanField(
        default = False
    )
    
    def __str__(self):
        return f'{self.code} | {self.user}'

class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length = 50
    )
    email = models.EmailField(
        unique = True
    )
    created_date = models.DateTimeField(
        auto_now_add = True
    )
    
    is_admin = models.BooleanField(
        default = False
    )
    score = models.PositiveIntegerField(default = 0)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
