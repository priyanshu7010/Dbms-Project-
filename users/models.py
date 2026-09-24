from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    u_age = models.IntegerField()
    pincode = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    passwords = models.CharField(max_length=100)

    class Meta:
        db_table = 'User'
        ordering = ['user_id']

    @property
    def user_age(self):
        return self.u_age

    @user_age.setter
    def user_age(self, val):
        self.u_age = val

    @property
    def password(self):
        return self.passwords

    @password.setter
    def password(self, val):
        self.passwords = val

    def __str__(self):
        return f"{self.user_id} - {self.user_name}"


class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    game_name = models.CharField(max_length=150)
    game_type = models.CharField(max_length=100)
    age_rest = models.IntegerField()
    rate = models.IntegerField()

    class Meta:
        db_table = 'Game'
        ordering = ['game_id']

    def __str__(self):
        return f"{self.game_name} ({self.game_type})"
