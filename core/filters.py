from django_filters import FilterSet
from .models import Card, Deck

class CardFilter(FilterSet):
    class Meta:
        model = Card
        fields = ['title']

class DeckFilter(FilterSet):
    class Meta:
        model = Deck
        fields = ['user', 'title', 'deck_format']