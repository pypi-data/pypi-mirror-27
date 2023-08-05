from cms.models import CMSPlugin

from django.db import models
from django.utils.translation import ugettext_lazy as _


class LiquidColumnsPluginModel(CMSPlugin):
    """
    Liquid columns
    """

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    COLUMNS_CHOICES = (
        (TWO, _('Two')),
        (THREE, _('Three')),
        (FOUR, _('Four')),
        (FIVE, _('Five')),
        (SIX, _('Six')),
    )

    num_columns = models.IntegerField(
        _('columns'),
        choices=COLUMNS_CHOICES,
        default=TWO,
        help_text=_('How many columns for this section?')
    )

    def __str__(self):
        return str(self.num_columns)

    class Meta:
        verbose_name = _('Liquid columns')
        verbose_name_plural = _('Liquid columns')
