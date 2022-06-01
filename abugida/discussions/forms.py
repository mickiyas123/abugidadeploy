from xml.etree.ElementInclude import include
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Questions, Answers




class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class QuestionForm(ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'
        exclude = ['user','topic']

class AnswerForm(ModelForm):
    class Meta:
        model = Answers
        fields = '__all__'
        execlude = ['user','room', 'question']

class QuestionRoomForm(ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'
        exclude = ['user','topic', 'room']

