from django.contrib import admin

# Register your models here.


from .models import Room, Topic, Message, User

#we want to see it in admin panel and also work with it in the built in admin panel
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)