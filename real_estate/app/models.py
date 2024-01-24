from django.db import models
from django.contrib.auth.hashers import make_password

class UserTable(models.Model):
    user_id = models.TextField(primary_key=True)
    firstname = models.TextField()
    lastname = models.TextField()
    created_at = models.DateField()
    password = models.CharField(max_length=20,null=True)
    email = models.TextField()

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Property(models.Model):
    property_id = models.TextField(primary_key=True)
    property_owner_id = models.ForeignKey(UserTable,on_delete=models.PROTECT)
    features = models.TextField()
    propertyimage_link = models.TextField()
    addressline1 = models.TextField()
    pincode = models.IntegerField()
    created_at = models.DateField()
    city = models.TextField()
    state = models.TextField()
    country = models.TextField()


class Units(models.Model):
    unit_id = models.AutoField(primary_key=True)
    unit_size = models.IntegerField()
    property_id = models.ForeignKey(Property, on_delete=models.PROTECT)
    created_at = models.DateField()
    unit_bhk_size = models.TextField()
    rent_value =models.IntegerField()



class TenentRentAggriment(models.Model):
    tenent_id = models.ForeignKey(UserTable, on_delete=models.PROTECT)
    units = models.ForeignKey(Units, on_delete=models.PROTECT)
    rent_value = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class Documents(models.Model):
    document_name = models.TextField()
    document_path = models.TextField()
    isverified = models.BooleanField()
    user_id = models.ForeignKey(UserTable, on_delete=models.CASCADE)


