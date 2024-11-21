from django.db import models


class TypeChoices(models.TextChoices):
    advice = "Advice", "Advice"
    question = "Question", "Question"
    story = "Story", "Story"
    other = "Other", "Other"
