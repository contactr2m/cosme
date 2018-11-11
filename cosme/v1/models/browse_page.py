from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager

from cosme.v1 import blocks as v1_blocks
from cosme.v1.atomic_elements import molecules, organisms
from cosme.v1.models.base import COSMEPage
from cosme.v1.util.util import get_secondary_nav_items


class BrowsePage(COSMEPage):
    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", molecules.FeaturedContent()),
        ],
        blank=True,
    )

    content = StreamField(
        [
            ("info_unit_group", organisms.InfoUnitGroup()),
            ("well", organisms.Well()),
            ("full_width_text", organisms.FullWidthText()),
            ("expandable", organisms.Expandable()),
            ("expandable_group", organisms.ExpandableGroup()),
            (
                "table_block",
                organisms.AtomicTableBlock(table_options={"renderer": "html"}),
            ),
            ("feedback", v1_blocks.Feedback()),
            ("raw_html_block", blocks.RawHTMLBlock(label="Raw HTML block")),
            ("html_block", organisms.HTMLBlock()),
            ("snippet_list", organisms.SnippetList()),
            ("image_text_25_75_group", organisms.ImageText2575Group()),
            ("image_text_50_50_group", organisms.ImageText5050Group()),
            ("half_width_link_blob_group", organisms.HalfWidthLinkBlobGroup()),
            ("third_width_link_blob_group", organisms.ThirdWidthLinkBlobGroup()),
        ],
        blank=True,
    )

    secondary_nav_exclude_sibling_pages = models.BooleanField(default=False)

    # General content tab
    content_panels = COSMEPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]

    sidefoot_panels = COSMEPage.sidefoot_panels + [
        FieldPanel("secondary_nav_exclude_sibling_pages")
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(sidefoot_panels, heading="Sidebar"),
            ObjectList(COSMEPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "browse-basic/index.html"

    objects = PageManager()

    @property
    def page_js(self):
        return super(BrowsePage, self).page_js + ["secondary-navigation.js"]

    def get_context(self, request, *args, **kwargs):
        context = super(BrowsePage, self).get_context(request, *args, **kwargs)
        context.update({"get_secondary_nav_items": get_secondary_nav_items})
        return context
