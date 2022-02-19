from django.forms import ModelForm  
from .models import Room

from django.contrib.auth.models import User
#tu cemo naraviti form format


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' #tu stavis od room model sve stavke koje zelis da budu prikazane, s __all__ ce biti sve
        exclude = ['host', 'participants'] #koga iz nase liste u ovom slucaju all zelimo izbaciti da se ne prikazuje 


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        