# encoding: utf-8
from django.dispatch import Signal

post_published = Signal(providing_args=["post"])
