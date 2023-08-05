from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .models import ArticlePluginModel, SectionPluginModel


class ArticlePlugin(CMSPluginBase):
    model = ArticlePluginModel
    name = _('Article')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_articles/article.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super(ArticlePlugin, self).render(
            context, instance, placeholder
        )
        thumb_opts = {
            'width': settings.RIPIU_ARTICLES_IMAGE_WIDTH,
            'height': settings.RIPIU_ARTICLES_IMAGE_HEIGHT,
            'crop': settings.RIPIU_ARTICLES_IMAGE_CROP,
            'upscale': settings.RIPIU_ARTICLES_IMAGE_UPSCALE,
        }
        if instance.alignment:
            thumb_opts['alignment'] = instance.alignment
        if instance.thumbnail_option:
            if instance.thumbnail_option.width:
                thumb_opts['width'] = instance.thumbnail_option.width
            if instance.thumbnail_option.height:
                thumb_opts['height'] = instance.thumbnail_option.height
            thumb_opts['crop'] = instance.thumbnail_option.crop
            thumb_opts['upscale'] = instance.thumbnail_option.upscale
        thumb_opts['size'] = (
            thumb_opts['width'],
            thumb_opts['height'],
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'thumb_opts': thumb_opts,
        })
        return context


plugin_pool.register_plugin(ArticlePlugin)


class SectionPlugin(CMSPluginBase):
    model = SectionPluginModel
    name = _('Section')
    module = "Ri+"
    render_template = 'ripiu/cmsplugin_articles/section.html'
    allow_children = True

    def render(self, context, instance, placeholder):
        context = super(SectionPlugin, self).render(
            context, instance, placeholder
        )
        thumb_opts = {
            'width': settings.RIPIU_ARTICLES_IMAGE_WIDTH,
            'height': settings.RIPIU_ARTICLES_IMAGE_HEIGHT,
            'crop': settings.RIPIU_ARTICLES_IMAGE_CROP,
            'upscale': settings.RIPIU_ARTICLES_IMAGE_UPSCALE,
        }
        if instance.alignment:
            thumb_opts['alignment'] = instance.alignment
        if instance.thumbnail_option:
            if instance.thumbnail_option.width:
                thumb_opts['width'] = instance.thumbnail_option.width
            if instance.thumbnail_option.height:
                thumb_opts['height'] = instance.thumbnail_option.height
            thumb_opts['crop'] = instance.thumbnail_option.crop
            thumb_opts['upscale'] = instance.thumbnail_option.upscale
        thumb_opts['size'] = (
            thumb_opts['width'],
            thumb_opts['height'],
        )
        context.update({
            'instance': instance,
            'placeholder': placeholder,
            'thumb_opts': thumb_opts,
        })
        return context


plugin_pool.register_plugin(SectionPlugin)
