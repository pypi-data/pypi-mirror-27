from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from colorfield.fields import ColorField

TOP = 0
MIDDLE = 1
BOTTOM = 2


class LasagnaPlugin(CMSPlugin):
    """Lasagna container"""

    name = models.CharField(
        _('name'), max_length=400, default='', blank=True
    )

    def __str__(self):
        return self.name or ""

    class Meta:
        verbose_name = _('Lasagna')
        verbose_name_plural = _('Lasagna')


class ColorLayerPlugin(CMSPlugin):
    """Color layer"""

    color = ColorField(
        _('color'), null=False,
    )

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = _('Color layer')
        verbose_name_plural = _('Color layer')


class OpacityModifierPlugin(CMSPlugin):
    """Sets the opacity of its children"""

    opacity = models.PositiveSmallIntegerField(
        _('opacity (%)'),
        validators=[MaxValueValidator(100)]
    )

    def __str__(self):
        return _('%(opacity)d%%') % {
            'opacity': self.opacity
        }

    class Meta:
        verbose_name = _('Opacity modifier')
        verbose_name_plural = _('Opacity modifiers')


class VerticalAlignmentModifierPlugin(CMSPlugin):
    """sets the vertical alignment of its children"""

    ALIGN_LABELS = {
        TOP: _('top'),
        MIDDLE: _('middle'),
        BOTTOM: _('bottom'),
    }

    ALIGN_CHOICES = (
        (TOP, ALIGN_LABELS[TOP]),
        (MIDDLE, ALIGN_LABELS[MIDDLE]),
        (BOTTOM, ALIGN_LABELS[BOTTOM]),
    )

    alignment = models.PositiveSmallIntegerField(
        _('alignment'), choices=ALIGN_CHOICES, default=TOP
    )

    def __str__(self):
        return str(self.ALIGN_LABELS[self.alignment])

    class Meta:
        verbose_name = _('Vertical alignment modifier')
        verbose_name_plural = _('Vertical alignment modifiers')
