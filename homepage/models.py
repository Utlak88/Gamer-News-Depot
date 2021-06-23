from django.db import models


class Google(models.Model):
    g_query = models.TextField(default="null")
    query_iter = models.CharField(default="null")


class Dev(models.Model):

    dev_name = models.CharField(default="null")
    dev_order_pop = models.IntegerField(default=0)
    dev_slug = models.CharField(default="null")
    dev_location = models.CharField(default="null")
    dev_admin_div = models.TextField(default="null")
    dev_country = models.CharField(default="null")
    dev_est = models.IntegerField(default=0)
    dev_notes = models.TextField(default="null")
    dev_image = models.ImageField(default="default.jpg")
    dev_image_address = models.TextField(default="null")
    google_query = models.TextField(default="null")

    def __str__(self):
        return f"{self.dev_name}"

    def get_absolute_url(self):
        return f'/developers/{self.dev_slug}'


class Pub(models.Model):

    pub_name = models.CharField(default="null")
    pub_slug = models.CharField(default="null")
    pub_location = models.CharField(default="null")
    pub_est = models.IntegerField(default=0)
    pub_notes = models.TextField(default="null")
    pub_image = models.ImageField(default="default.jpg", upload_to="pub_pics")

    def __str__(self):
        return f"{self.pub_name}"
