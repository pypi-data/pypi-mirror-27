from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _

from .models import ArticlePluginModel, SectionPluginModel


class ArticlePlugin(CMSPluginBase):
    model = ArticlePluginModel
    name = _('Article')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_articles/article.html'
    allow_children = True


plugin_pool.register_plugin(ArticlePlugin)


class SectionPlugin(CMSPluginBase):
    model = SectionPluginModel
    name = _('Section')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_articles/section.html'
    allow_children = True


plugin_pool.register_plugin(SectionPlugin)
