from django.db import models
import uuid

class BaseModel(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Restaurant(BaseModel):

    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    categories = models.ManyToManyField("restaurant.Category")
    
    def __str__(self):
        return self.name + " in " + self.location


class Category(BaseModel):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    
class Item(BaseModel):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (" + str(self.category) + " / " + str(self.restaurant) + ")"


class Item_User_Relation(BaseModel):

    account = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
