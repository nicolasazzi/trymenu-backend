from django.contrib import admin
from .models import Restaurant, Category, Item, Item_User_Relation



admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Item_User_Relation) 