from django.utils import timezone
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='', help_text='Название на английском')
    title_jp = models.CharField(max_length=200, default='', help_text='Название на японском')
    image = models.ImageField(null=True)
    description = models.TextField(default='', help_text='Введите описание покемона')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()

    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)

    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=1)
    defence = models.IntegerField(default=10)
    stamina = models.IntegerField(default=5)
