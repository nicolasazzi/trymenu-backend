from django.db import models


class restaurant(models.Model):

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    category = models.ManyToManyField("restaurant.category")
    
    def __str__(self):
        return self.name + " in " + self.location


class category(models.Model):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    
class food(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    restaurant = models.ForeignKey(restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (" + self.category + " / " + self.restaurant + ")"