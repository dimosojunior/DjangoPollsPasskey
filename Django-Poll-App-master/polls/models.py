from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings



class Courses(models.Model):
    CourseName = models.CharField(max_length=500)

    def __str__(self):
        return self.CourseName

class Colleges(models.Model):
    CollegeName = models.CharField(max_length=500)

    def __str__(self):
        return self.CollegeName

class Location(models.Model):
    LocationName = models.CharField(max_length=500)

    def __str__(self):
        return self.LocationName


class Years(models.Model):
    Name = models.CharField(max_length=500)

    def __str__(self):
        return self.Name



class MyUserManager(BaseUserManager):
    def create_user(self, email,username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your username is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

    



class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone",default="+255", max_length=13)

    Course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True,null=True)
    Year = models.ForeignKey(Years, on_delete=models.CASCADE, blank=True,null=True)
    College = models.ForeignKey(Colleges, on_delete=models.CASCADE, blank=True,null=True)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True,null=True)
    
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="username"
    REQUIRED_FIELDS=['email']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True













class ElectionCategories(models.Model):
    Category = models.CharField(max_length=500)

    def __str__(self):
        return self.Category

class Poll(models.Model):
    Category = models.ForeignKey(ElectionCategories, on_delete=models.CASCADE)
    Course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True,null=True)
    Year = models.ForeignKey(Years, on_delete=models.CASCADE, blank=True,null=True)
    College = models.ForeignKey(Colleges, on_delete=models.CASCADE, blank=True,null=True)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    is_off_cumpus = models.BooleanField(default=False,blank=True,null=True)

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res

    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
