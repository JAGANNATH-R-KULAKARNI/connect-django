from django.contrib import admin
from my_app.models import Person
from my_app.models import Posts
# Register your models here.


admin.site.register(Person)
admin.site.register(Posts)