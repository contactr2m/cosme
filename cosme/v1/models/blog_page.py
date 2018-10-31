from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from .base import COSMEPageManager, AbstractFilterPage, v1_blocks, organisms


class BlogPage(AbstractFilterPage):
    content = StreamField([
        ('full_width_text', organisms.FullWidthText()),
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('expandable', organisms.Expandable()),
        ('well', organisms.Well()),
        ('email_signup', organisms.EmailSignUp()),
        ('feedback', v1_blocks.Feedback()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
    ])
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'

    objects = PageManager()
    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]


class LegacyBlogPage(AbstractFilterPage):
    content = StreamField([
        ('content', blocks.RawHTMLBlock(
            help_text='Content from WordPress unescaped.'
        )),
        ('feedback', v1_blocks.Feedback()),
    ])
    objects = COSMEPageManager()
    edit_handler = AbstractFilterPage.generate_edit_handler(
        content_panel=StreamFieldPanel('content')
    )
    template = 'blog/blog_page.html'

    search_fields = AbstractFilterPage.search_fields + [
        index.SearchField('content')
    ]
