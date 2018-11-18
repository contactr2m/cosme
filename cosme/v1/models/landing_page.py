from wagtail.admin.edit_handlers import (
    ObjectList, StreamFieldPanel, TabbedInterface
)
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager
from wagtail.search import index

from .. import blocks as v1_blocks
from ..atomic_elements import molecules, organisms
from ..models.base import COSMEPage


class LandingPage(COSMEPage):
    header = StreamField([
        ('hero', molecules.Hero()),
        ('text_introduction', molecules.TextIntroduction()),
    ], blank=True)

    content = StreamField([
        ('info_unit_group', organisms.InfoUnitGroup()),
        ('well', organisms.Well()),
        ('feedback', v1_blocks.Feedback()),
        ('image_text_25_75_group', organisms.ImageText2575Group()),
        ('image_text_50_50_group', organisms.ImageText5050Group()),
        ('half_width_link_blob_group', organisms.HalfWidthLinkBlobGroup()),
        ('third_width_link_blob_group', organisms.ThirdWidthLinkBlobGroup()),
    ], blank=True)

    # General content tab
    content_panels = COSMEPage.content_panels + [
        StreamFieldPanel('header'),
        StreamFieldPanel('content'),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='General Content'),
        ObjectList(COSMEPage.sidefoot_panels, heading='Sidebar'),
        ObjectList(COSMEPage.settings_panels, heading='Configuration'),
    ])

    template = 'landing-page/index.html'

    objects = PageManager()

    search_fields = COSMEPage.search_fields + [
        index.SearchField('content'),
        index.SearchField('header')
    ]
