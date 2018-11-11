from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager

from cosme.v1 import blocks as v1_blocks
from cosme.v1.atomic_elements import molecules, organisms
from cosme.v1.feeds import FilterableFeedPageMixin
from cosme.v1.models.base import COSMEPage
from cosme.v1.util.filterable_list import FilterableListMixin


class BrowseFilterablePage(FilterableFeedPageMixin, FilterableListMixin, COSMEPage):
    header = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("featured_content", molecules.FeaturedContent()),
        ]
    )
    content = StreamField(
        [
            ("full_width_text", organisms.FullWidthText()),
            ("filter_controls", organisms.FilterControls()),
            ("feedback", v1_blocks.Feedback()),
        ]
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
            ObjectList(sidefoot_panels, heading="SideFoot"),
            ObjectList(COSMEPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "browse-filterable/index.html"

    objects = PageManager()

    @property
    def page_js(self):
        return super(BrowseFilterablePage, self).page_js + ["secondary-navigation.js"]


class EventArchivePage(BrowseFilterablePage):
    template = "browse-filterable/index.html"

    objects = PageManager()

    @staticmethod
    def get_form_class():
        from .. import forms

        return forms.EventArchiveFilterForm


class NewsroomLandingPage(BrowseFilterablePage):
    template = "newsroom/index.html"
    filterable_categories = ("Blog", "Newsroom")
    filterable_children_only = False

    objects = PageManager()
