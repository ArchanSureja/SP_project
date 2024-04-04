from django import template
import os

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value)


@register.filter
def extract_labels(user_notes):
    labels = set()
    for note in user_notes:
        labels.add(note.label)
    return sorted(labels)