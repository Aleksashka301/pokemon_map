import folium

from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()

    for pokemon in Pokemon.objects.all():
        for pokemon_entity in PokemonEntity.objects.filter(
            appeared_at__lte=current_time,
            disappeared_at__gte=current_time,
        ):
            image_url = request.build_absolute_uri(pokemon.image.url)
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                image_url
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    image_url = request.build_absolute_uri(pokemon.image.url)
    current_time = localtime()

    previous_pokemon = None
    if pokemon.previous_evolution:
        previous_pokemon = {
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
            'id': pokemon.previous_evolution.id
        }

    next_pokemon = []
    for evolution in pokemon.next_evolution.all():  # next_evolutions - related_name
        next_pokemon.append({
            'title_ru': evolution.title,
            'img_url': request.build_absolute_uri(evolution.image.url),
            'id': evolution.id
        })

    requested_pokemon = {
        'title_ru': pokemon.title,
        'img_url': image_url,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'previous_evolution': previous_pokemon,
        'next_evolution': next_pokemon,
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(
            pokemon=pokemon,
            appeared_at__lte=current_time,
            disappeared_at__gte=current_time,
    ):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            requested_pokemon['img_url'],
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon
    })



