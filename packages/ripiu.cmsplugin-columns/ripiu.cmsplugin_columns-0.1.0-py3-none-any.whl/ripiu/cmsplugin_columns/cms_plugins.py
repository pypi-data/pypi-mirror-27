from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from .models import LiquidColumnsPluginModel


class LiquidColumnsPlugin(CMSPluginBase):
    """
    Liquid columns
    """
    model = LiquidColumnsPluginModel
    name = _('Liquid columns')
    module = _('Multi Columns')
    render_template = 'ripiu/cmsplugin_columns/columns.html'
    allow_children = True


plugin_pool.register_plugin(LiquidColumnsPlugin)
