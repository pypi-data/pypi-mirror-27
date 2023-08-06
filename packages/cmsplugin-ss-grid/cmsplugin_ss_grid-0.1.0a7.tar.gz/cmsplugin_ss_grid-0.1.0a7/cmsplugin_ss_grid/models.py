from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField
from cms.models import CMSPlugin
from cms.utils.compat.dj import python_2_unicode_compatible

from .fields import ColorPickerField

CONFIG = getattr(settings, 'CMSPLUGIN_SS_GRID', {})

CELL_DEFAULT_CLASS = CONFIG.get('CELL_DEFAULT_CLASS')

INHERIT = 0
SMALL_CELL_WIDTHS = [(w, str(w)) for w in range(1, 13)]
CELL_WIDTHS = [(INHERIT, 'Inherit')] + SMALL_CELL_WIDTHS


class StyleMixin(object):
    STYLE_FIELDS = []

    @property
    def style(self):
        rv = []

        for field_name in self.STYLE_FIELDS:
            if getattr(self, field_name):
                style_name = field_name.replace('_', '-')
                rv.append('{}:{}'.format(style_name, getattr(self, field_name)))
        return ';'.join(rv)


class PaddingMixin(models.Model):
    STYLE_FIELDS = [
        'padding_top',
        'padding_right',
        'padding_bottom',
        'padding_left'
    ]

    class Meta():
        abstract = True

    padding_top = models.CharField(
        _('Padding Top'), null=True, blank=True, max_length=50
    )

    padding_right = models.CharField(
        _('Padding Right'), null=True, blank=True, max_length=50
    )

    padding_bottom = models.CharField(
        _('Padding Bottom'), null=True, blank=True, max_length=50
    )

    padding_left = models.CharField(
        _('Padding Left'), null=True, blank=True, max_length=50
    )


class MarginMixin(models.Model):
    STYLE_FIELDS = [
        'margin_top',
        'margin_right',
        'margin_bottom',
        'margin_left'
    ]

    class Meta():
        abstract = True

    margin_top = models.CharField(
        _('Margin Top'), null=True, blank=True, max_length=50
    )

    margin_right = models.CharField(
        _('Margin Right'), null=True, blank=True, max_length=50
    )

    margin_bottom = models.CharField(
        _('Margin Bottom'), null=True, blank=True, max_length=50
    )

    margin_left = models.CharField(
        _('Margin Left'), null=True, blank=True, max_length=50
    )


@python_2_unicode_compatible
class Container(StyleMixin, PaddingMixin, CMSPlugin):
    STYLE_FIELDS = PaddingMixin.STYLE_FIELDS + ['background_color']

    background_image = FilerImageField(
        verbose_name=_('Background Image'),
        null=True,
        blank=True
    )
    background_color = ColorPickerField(
        verbose_name=_('Background Colour'),
        null=True,
        blank=True,
        help_text=_('This can be seen while the image loads or if there is no image')
    )
    background_class = models.CharField(
        _('Background Class'),
        blank=True, null=True,
        max_length=255
    )
    background_id = models.CharField(
        _('Background ID'),
        blank=True, null=True,
        max_length=255,
        help_text=_('ID applied to the background HTML element')
    )

    @property
    def background_classes(self):
        return self.background_class or ''

    @property
    def background_style(self):
        rv = [self.style]
        if self.background_image:
            rv.append("background-image:url('{}')".format(self.background_image.url))
        return ';'.join(rv)

    def __str__(self):
        rv = []
        if self.background_id:
            rv.append('#{}'.format(self.background_id))
        if self.background_class:
            rv.append('.{}'.format(self.background_class))
        return ' '.join(rv)


@python_2_unicode_compatible
class ContainerCell(StyleMixin, PaddingMixin, MarginMixin, CMSPlugin):
    STYLE_FIELDS = PaddingMixin.STYLE_FIELDS + MarginMixin.STYLE_FIELDS

    size_mobile = models.IntegerField(
        _('Size Mobile'),
        choices=SMALL_CELL_WIDTHS,
        default=12
    )

    size_tablet = models.IntegerField(
        _('Size Tablet'),
        choices=CELL_WIDTHS,
        default=INHERIT
    )

    size_desktop = models.IntegerField(
        _('Size Desktop'),
        choices=CELL_WIDTHS,
        default=INHERIT
    )

    size_large_desktop = models.IntegerField(
        _('Size Large Desktop'),
        choices=CELL_WIDTHS,
        default=INHERIT
    )

    custom_class = models.CharField(
        _('Class'),
        blank=True, null=True,
        max_length=255
    )

    @property
    def css_classes(self):
        rv = []
        if CELL_DEFAULT_CLASS:
            rv.append(CELL_DEFAULT_CLASS)
        rv.append('col-sm-{}'.format(self.size_mobile))
        if self.size_tablet:
            rv.append('col-md-{}'.format(self.size_tablet))
        if self.size_desktop:
            rv.append('col-lg-{}'.format(self.size_desktop))
        if self.size_large_desktop:
            rv.append('col-xl-{}'.format(self.size_large_desktop))
        if self.custom_class:
            rv.append(self.custom_class)

        return ' '.join(rv)

    def __str__(self):
        rv = ['Mobile {}'.format(self.size_mobile)]
        if self.size_tablet:
            rv.append('Tablet {}'.format(self.size_tablet))
        if self.size_desktop:
            rv.append('Desktop {}'.format(self.size_desktop))
        if self.size_large_desktop:
            rv.append('Large Desktop {}'.format(self.size_large_desktop))

        return '; '.join(rv)
