from wagtail.admin.edit_handlers import ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager

from cosme.v1 import blocks as v1_blocks
from cosme.v1.atomic_elements import molecules, organisms
from cosme.v1.feeds import FilterableFeedPageMixin
from cosme.v1.models.base import COSMEPage
from cosme.v1.util.filterable_list import FilterableListMixin


class SublandingFilterablePage(FilterableFeedPageMixin, FilterableListMixin, COSMEPage):
    header = StreamField([("hero", molecules.Hero())], blank=True)
    content = StreamField(
        [
            ("text_introduction", molecules.TextIntroduction()),
            ("full_width_text", organisms.FullWidthText()),
            ("filter_controls", organisms.FilterControls()),
            ("featured_content", molecules.FeaturedContent()),
            ("feedback", v1_blocks.Feedback()),
        ]
    )

    # General content tab
    content_panels = COSMEPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("content"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(COSMEPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(COSMEPage.settings_panels, heading="Configuration"),
        ]
    )

    template = "sublanding-page/index.html"

    objects = PageManager()


class ActivityLogPage(SublandingFilterablePage):
    template = "activity-log/index.html"
    filterable_categories = ("Blog", "Newsroom", "Research Report")
    filterable_children_only = False
    filterable_per_page_limit = 100

    objects = PageManager()
