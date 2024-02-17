from django.db import models


class Color(models.Model):
    color_name = models.CharField(max_length = 50)
    color_hex = models.CharField(max_length=20)

    def __str__(self):
        return self.color_name


class Person(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color', null=True, blank=True)
    # col_hex = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='col_hex', null=True, blank=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
