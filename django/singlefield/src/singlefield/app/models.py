from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    misc = models.JSONField(
        help_text='Stored as JSON',
        default=dict,
        blank=True,
    )

    def get_misc_keys(self):
        return tuple(self.object.misc.keys())
