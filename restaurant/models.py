from django.db import models


class Restaurant(models.Model):

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    categories = models.ManyToManyField("restaurant.Category")
    
    def __str__(self):
        return self.name + " in " + self.location


class Category(models.Model):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    
class Item(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (" + str(self.category) + " / " + str(self.restaurant) + ")"


class Item_User_Relation(models.Model):

    did_try = models.BooleanField(default=False)
    account = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
