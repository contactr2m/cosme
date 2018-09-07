from wagtail.admin.edit_handlers import ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.blocks import ListBlock, StructBlock, DateTimeBlock, ChoiceBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import PageManager

from cosme.v1.atomic_elements import atoms, molecules
from cosme.v1.models.base import COSMEPage
from cosme.v1.util import ref


class HomePage(COSMEPage):
    header = StreamField(
        [
            ("info_unit", molecules.InfoUnit()),
            ("half_width_link_blob", molecules.HalfWidthLinkBlob()),
        ],
        blank=True,
    )

    latest_updates = StreamField(
        [
            (
                "posts",
                ListBlock(
                    StructBlock(
                        [
                            (
                                "categories",
                                ChoiceBlock(
                                    choices=ref.limited_categories, required=False
                                ),
                            ),
                            ("link", atoms.Hyperlink()),
                            ("date", DateTimeBlock(required=False)),
                        ]
                    )
                ),
            )
        ],
        blank=True,
    )

    # General content tab
    content_panels = COSMEPage.content_panels + [
        StreamFieldPanel("header"),
        StreamFieldPanel("latest_updates"),
    ]

    # Tab handler interface
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="General Content"),
            ObjectList(COSMEPage.sidefoot_panels, heading="Sidebar"),
            ObjectList(COSMEPage.settings_panels, heading="Configuration"),
        ]
    )

    # Sets page to only be creatable at the root
    parent_page_types = ["wagtailcore.Page"]

    template = "index.html"

    objects = PageManager()

    def get_category_name(self, category_icon_name):
        cats = dict(ref.limited_categories)
        return cats[str(category_icon_name)]

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request)
        return context
