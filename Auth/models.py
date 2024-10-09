from django.db import models

# Create your models here.

class Auth(models.Model):
    Username=models.CharField(max_length=255 , blank=False)
    Email = models.EmailField(max_length=50, blank=False)
    Password = models.CharField(max_length=128 , blank=False)  

    def __str__(self):
        return self.Email



class ActivationCode(models.Model):
    ID = models.AutoField(primary_key=True)
    AuthID = models.ForeignKey(Auth, on_delete=models.CASCADE)
    ActivationCode = models.CharField(max_length=11, blank=False)

    def __str__(self):
        return self.ActivationCode


class Profile(models.Model):
    ID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Auth, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=50, blank=False)
    LastName = models.CharField(max_length=50, blank=False)
    BusinessName = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f'{self.FirstName} {self.LastName}'
