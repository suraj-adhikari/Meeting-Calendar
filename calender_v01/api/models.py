from django.db import models

# Create your models here.
class userData(models.Model):
    userName=models.CharField(max_length=250)
    emailId=models.EmailField()
    password1=models.CharField(max_length=250)
    password2=models.CharField(max_length=250)
    apiKey=models.CharField(max_length=1000)

    def __str__(self) -> str:
        return (self.emailId)
    
class formData(models.Model):
    formId=models.CharField(max_length=250)
    apiKey=models.CharField(max_length=1000,default=0)
    name=models.CharField(max_length=250)
    createdAt=models.DateTimeField()
    updatedAt=models.DateTimeField()
    count=models.IntegerField(null=True)

    
    def __str__(self) -> str:
        return (self.name)
