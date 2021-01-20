from django.db import models


class Products(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='Music/images', default="")

    def __str__(self):
        return self.product_name
