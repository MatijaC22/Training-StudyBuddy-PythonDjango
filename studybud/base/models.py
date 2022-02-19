from django.db import models

from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


#PAZI: AKO SI STAVIO CALSSU TOPIC ispod Rooma u Room topic = \.... ForeignKey('Topic') moras staviti u navodnike topic (django pravilo) 

class Room(models.Model):
    host= models.ForeignKey(User , on_delete=models.SET_NULL, null=True) #moramo staviti null=true jer moramo dozvoliti da ako ga neko pobrise da moze biti prazan
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL, null=True) #moramo staviti null=true jer moramo dozvoliti da ako ga neko pobrise da moze biti prazan
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #null is allowed/ to mjesto moze ostati prazn, jer inace to nije dozvoljeno ako ne navedes -- balnk= true --> ako runamo save method this we can leave empty
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #svaki put kada save-mo novi podatak ovdje ce biti zapisani detalji kada se to desilo
    #everytime the save method is called go ahead and take a timestamp
    created = models.DateTimeField(auto_now_add=True)
    #razlika auto_now i auto_now_add --> auto_now update everytime we make change; auto_now_add only when we first create this instance

    class Meta:  #Model Meta is basically used to change the behavior of your model fields like changing order options,verbose_name and lot of other options
        ordering = ['-updated', '-created'] #reverse ordering tako da najnoviji update i created bude na vrhu liste 

    def __str__(self): #The __str__ method in Python represents the class objects as a string – it can be used for classes. The __str__ method should be defined in a way that is easy to read and outputs all the members of the class. This method is also used as a debugging tool when the members of a class need to be checked.
        return self.name #creating string version

class Message(models.Model):
    #ForeignKey je metoda za many-to-one Relationship
    user= models.ForeignKey(User, on_delete=models.CASCADE) #user model koji se importa iz django.contrib.auth. pogledaj na vrh i trazi na internetu
    #user moze imati puno messages ali message moze imati samo jednog usera
    room = models.ForeignKey(Room , on_delete=models.CASCADE) #kada neko makne parent room zelimo pobrisati kid od rooma, mozemo staviti  SET_NULL u tom slucaju bi stavio nula ne pobrisao totalno room
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #svaki put kada save-mo novi podatak ovdje ce biti zapisani detalji kada se to desilo
    created = models.DateTimeField(auto_now_add=True)

    class Meta:  #Model Meta is basically used to change the behavior of your model fields like changing order options,verbose_name and lot of other options
        ordering = ['-updated', '-created'] #reverse ordering tako da najnoviji update i created bude na vrhu liste 

    def __str__(self):
        return self.body[0:50]
    
    