from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Questions, Answers

admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Questions)
admin.site.register(Answers)