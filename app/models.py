from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Poi(models.Model):
    name = models.CharField(max_length=50)
    external_id = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pois"
    )
    avg_rating = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.name
