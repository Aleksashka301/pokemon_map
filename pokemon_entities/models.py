from django.utils import timezone
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Имя покемона:', max_length=200)
    title_en = models.CharField('Имя покемона на анг.:', max_length=200)
    title_jp = models.CharField('Имя покемона на яп.:', max_length=200)
    image = models.ImageField('Картинка покемона:', null=True)
    description = models.TextField('Описание покемона:', default='')
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolution',
        verbose_name='Предок покемона:'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон:')
    lat = models.FloatField('Широта:')
    lon = models.FloatField('Долгота:')

    appeared_at = models.DateTimeField('Дата и время появления покемона:', default=timezone.now)
    disappeared_at = models.DateTimeField('Дата и время исчезновения покемона:')

    level = models.IntegerField('Уровень покемона:', default=1)
    health = models.IntegerField('Жизнь покемона:', default=100)
    strength = models.IntegerField('Сила покемона:', default=1)
    defence = models.IntegerField('Защита покемона:', default=10)
    stamina = models.IntegerField('Выносливость покемона:', default=5)
