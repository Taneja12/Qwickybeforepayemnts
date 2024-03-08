from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    price = models.CharField(max_length=20)
    product_id = models.CharField(max_length=30,unique=True)
    img = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.product_id

