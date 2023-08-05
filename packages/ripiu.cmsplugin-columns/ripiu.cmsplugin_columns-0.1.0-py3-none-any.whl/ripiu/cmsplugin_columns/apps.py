# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ColumnsConfig(AppConfig):
    name = 'ripiu.cmsplugin_columns'
    verbose_name = _('Liquid columns')
