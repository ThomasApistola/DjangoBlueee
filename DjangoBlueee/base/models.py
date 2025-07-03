from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
 
 
# Create your models here.
class Profile(models.Model):
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.user.username
   
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    cures = models.CharField(max_length=100)
    sideEffects = models.TextField()
   
    def __str__(self):
        return self.name
 
class Collection(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=False,)
    collected = models.BooleanField(default=False)
    collected_approved = models.BooleanField(default=False)
    collected_approved_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                                              related_name='approved_collections', null=True, blank=True)
 
    def __str__(self):
        return f"{self.user.username} - {self.medicine.name} ({self.date})"
   
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
 
 
 