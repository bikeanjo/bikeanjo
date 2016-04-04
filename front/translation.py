from modeltranslation.translator import translator, TranslationOptions
from front.models import (Event, TipForCycling, Testimony)
from django.contrib.flatpages.models import FlatPage


class EventTranslationOptions(TranslationOptions):
    fields = ['title', 'content', 'address', 'subscription_link', 'price']


translator.register(Event, EventTranslationOptions)


class FlatPageTranslationOptions(TranslationOptions):
    fields = ['title', 'content']


translator.register(FlatPage, FlatPageTranslationOptions)


class TipForCyclingTranslationOptions(TranslationOptions):
    fields = ['title', 'content']


translator.register(TipForCycling, TipForCyclingTranslationOptions)


class TestimonyTranslationOptions(TranslationOptions):
    fields = ['message']

translator.register(Testimony, TestimonyTranslationOptions)