from six.moves.urllib.parse import urlencode

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone, translation
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, ObjectList,
                                         StreamFieldPanel, TabbedInterface)
from wagtail.core import hooks
from wagtail.core.fields import StreamField
from wagtail.core.models import (Orderable, Page, PageManager, PageQuerySet)
from wagtail.images.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtailinventory.helpers import get_page_blocks

from cosme.v1.util import ref
from cosme.v1.atomic_elements import molecules, organisms
from cosme.v1 import blocks as v1_blocks
from cosme.v1.models.snippets import ReusableText
from cosme.v1.models.images import COSMEImage


class COSMEAuthoredPages(TaggedItemBase):
    content_object = ParentalKey('COSMEPage')

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class COSMETaggedPages(TaggedItemBase):
    content_object = ParentalKey('COSMEPage')

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class BaseCOSMEPageManager(PageManager):
    def get_queryset(self):
        return PageQuerySet(self.model).order_by('path')


COSMEPageManager = BaseCOSMEPageManager.from_queryset(PageQuerySet)


class COSMEPage(Page):
    authors = ClusterTaggableManager(through=COSMEAuthoredPages, blank=True,
                                     verbose_name='Authors',
                                     help_text='A comma separated list of '
                                               + 'authors.',
                                     related_name='authored_pages')
    tags = ClusterTaggableManager(through=COSMETaggedPages, blank=True,
                                  related_name='tagged_pages')
    shared = models.BooleanField(default=False)
    has_unshared_changes = models.BooleanField(default=False)
    language = models.CharField(
        choices=ref.supported_languagues, default='en', max_length=2
    )
    social_sharing_image = models.ForeignKey(
        'COSMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=(
            'Optionally select a custom image to appear when users share this '
            'page on social media websites. Recommended size: 1200w x 630h. '
            'Maximum size: 4096w x 4096h.'
        )
    )

    # This is used solely for subclassing pages we want to make at the CFPB.
    is_creatable = False

    objects = COSMEPageManager()

    # These fields show up in either the sidebar or the footer of the page
    # depending on the page type.
    sidefoot = StreamField([
        ('call_to_action', molecules.CallToAction()),
        ('related_links', molecules.RelatedLinks()),
        ('related_posts', organisms.RelatedPosts()),
        ('related_metadata', molecules.RelatedMetadata()),
        ('email_signup', organisms.EmailSignUp()),
        ('sidebar_contact', organisms.SidebarContactInfo()),
        ('rss_feed', molecules.RSSFeed()),
        ('social_media', molecules.SocialMedia()),
        ('reusable_text', v1_blocks.ReusableTextChooserBlock(ReusableText)),
    ], blank=True)

    # Panels
    promote_panels = Page.promote_panels + [
        ImageChooserPanel('social_sharing_image'),
    ]

    sidefoot_panels = [
        StreamFieldPanel('sidefoot'),
    ]

    settings_panels = [
        MultiFieldPanel(promote_panels, 'Settings'),
        InlinePanel('categories', label="Categories", max_num=2),
        FieldPanel('tags', 'Tags'),
        FieldPanel('authors', 'Authors'),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
        FieldPanel('language', 'language'),
    ]

    # Tab handler interface guide because it must be repeated for each subclass
    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='General Content'),
        ObjectList(sidefoot_panels, heading='Sidebar/Footer'),
        ObjectList(settings_panels, heading='Configuration'),
    ])

    def clean(self):
        super(COSMEPage, self).clean()
        # validate_social_sharing_image(self.social_sharing_image)

    def get_authors(self):
        """ Returns a sorted list of authors. Default is alphabetical """
        return self.alphabetize_authors()

    def alphabetize_authors(self):
        """
        Alphabetize authors of this page by last name,
        then first name if needed
        """
        # First sort by first name
        author_names = self.authors.order_by('name')
        # Then sort by last name
        return sorted(author_names, key=lambda x: x.name.split()[-1])

    def generate_view_more_url(self, request):
        """Generate a URL to see more pages like this one.
        This method generates a link to the Activity Log page (which must
        exist and must have a unique site-wide slug of "activity-log") with
        filters set by the tags assigned to this page, like this:
        /activity-log/?topics=foo&topics=bar&topics=baz
        If for some reason a page with slug "activity-log" does not exist,
        this method will raise Page.DoesNotExist.
        """
        activity_log = Page.objects.get(slug='activity-log')
        url = activity_log.get_url(request)

        tags = urlencode([('topics', tag) for tag in self.tags.slugs()])
        if tags:
            url += '?' + tags

        return url

    def related_posts(self, block):
        # from v1.models.learn_page import AbstractFilterPage

        def tag_set(related_page):
            return set([tag.pk for tag in related_page.tags.all()])

        def match_all_topic_tags(queryset, page_tags):
            """Return pages that share every one of the current page's tags."""
            current_tag_set = set([tag.pk for tag in page_tags])
            return [page for page in queryset
                    if current_tag_set.issubset(tag_set(page))]

        related_types = []
        related_items = {}
        if block.value.get('relate_posts'):
            related_types.append('blog')
        if block.value.get('relate_newsroom'):
            related_types.append('newsroom')
        if block.value.get('relate_events'):
            related_types.append('events')
        if not related_types:
            return related_items

        tags = self.tags.all()
        and_filtering = block.value['and_filtering']
        specific_categories = block.value['specific_categories']
        limit = int(block.value['limit'])
        queryset = AbstractFilterPage.objects.live().exclude(
            id=self.id).order_by('-date_published').distinct()

        for parent in related_types:  # blog, newsroom or events
            # Include children of this slug that match at least 1 tag
            children = Page.objects.child_of_q(Page.objects.get(slug=parent))
            filters = children & Q(('tags__in', tags))

            if parent == 'events':
                # Include archived events matches
                archive = Page.objects.get(slug='archive-past-events')
                children = Page.objects.child_of_q(archive)
                filters |= children & Q(('tags__in', tags))

            if specific_categories:
                # Filter by any additional categories specified
                categories = ref.get_appropriate_categories(
                    specific_categories=specific_categories,
                    page_type=parent
                )
                if categories:
                    filters &= Q(('categories__name__in', categories))

            related_queryset = queryset.filter(filters)

            if and_filtering:
                # By default, we need to match at least one tag
                # If specified in the admin, change this to match ALL tags
                related_queryset = match_all_topic_tags(related_queryset, tags)

            related_items[parent.title()] = related_queryset[:limit]

        # Return items in the dictionary that have non-empty querysets
        return {key: value for key, value in related_items.items() if value}

    def related_metadata_tags(self):
        # Set the tags to correct data format
        tags = {'links': []}
        filter_page = self.get_filter_data()
        for tag in self.specific.tags.all():
            tag_link = {'text': tag.name, 'url': ''}
            if filter_page:
                relative_url = filter_page.relative_url(filter_page.get_site())
                param = '?topics=' + tag.slug
                tag_link['url'] = relative_url + param
            tags['links'].append(tag_link)
        return tags

    def get_filter_data(self):
        for ancestor in self.get_ancestors().reverse().specific():
            if ancestor.specific_class.__name__ in ['BrowseFilterablePage',
                                                    'SublandingFilterablePage',
                                                    'EventArchivePage',
                                                    'NewsroomLandingPage']:
                return ancestor
        return None

    def get_breadcrumbs(self, request):
        ancestors = self.get_ancestors()
        home_page_children = request.site.root_page.get_children()
        for i, ancestor in enumerate(ancestors):
            if ancestor in home_page_children:
                # Add top level parent page and `/process/` url segments
                # where necessary to OAH page breadcrumbs.
                return [ancestor for ancestor in ancestors[i + 1:]]
        return []

    def get_appropriate_descendants(self, inclusive=True):
        return COSMEPage.objects.live().descendant_of(self, inclusive)

    def get_appropriate_siblings(self, inclusive=True):
        return COSMEPage.objects.live().sibling_of(self, inclusive)

    def get_context(self, request, *args, **kwargs):
        context = super(COSMEPage, self).get_context(request, *args, **kwargs)
        for hook in hooks.get_hooks('cfgovpage_context_handlers'):
            hook(self, request, context, *args, **kwargs)
        return context

    def serve(self, request, *args, **kwargs):
        """
        If request is ajax, then return the ajax request handler response, else
        return the super.
        """
        if request.method == 'POST':
            return self.serve_post(request, *args, **kwargs)

        # Force the page's language on the request
        translation.activate(self.language)
        request.LANGUAGE_CODE = translation.get_language()
        return super(COSMEPage, self).serve(request, *args, **kwargs)

    def _return_bad_post_response(self, request):
        if request.is_ajax():
            return JsonResponse({'result': 'error'}, status=400)

        return HttpResponseBadRequest(self.url)

    def serve_post(self, request, *args, **kwargs):
        """Handle a POST to a specific form on the page.
        Attempts to retrieve form_id from the POST request, which must be
        formatted like "form-name-index" where the "name" part is the name of a
        StreamField on the page and the "index" part refers to the index of the
        form element in the StreamField.
        If form_id is found, it returns the response from the block method
        retrieval.
        If form_id is not found, it returns an error response.
        """
        form_module = None
        form_id = request.POST.get('form_id', None)

        if form_id:
            form_id_parts = form_id.split('-')

            if len(form_id_parts) == 3:
                streamfield_name = form_id_parts[1]
                streamfield = getattr(self, streamfield_name, None)

                if streamfield is not None:
                    try:
                        streamfield_index = int(form_id_parts[2])
                    except ValueError:
                        streamfield_index = None

                    try:
                        form_module = streamfield[streamfield_index]
                    except IndexError:
                        form_module = None

        if form_module is None:
            return self._return_bad_post_response(request)

        result = form_module.block.get_result(
            self,
            request,
            form_module.value,
            True
        )

        if isinstance(result, HttpResponse):
            return result

        context = self.get_context(request, *args, **kwargs)
        context['form_modules'][streamfield_name].update({
            streamfield_index: result
        })

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            context
        )

    class Meta:
        app_label = 'v1'

    def parent(self):
        parent = self.get_ancestors(inclusive=False).reverse()[0].specific
        return parent

    # To be overriden if page type requires JS files every time
    @property
    def page_js(self):
        return []

    @property
    def streamfield_js(self):
        js = []

        block_cls_names = get_page_blocks(self)
        for block_cls_name in block_cls_names:
            block_cls = import_string(block_cls_name)
            if hasattr(block_cls, 'Media') and hasattr(block_cls.Media, 'js'):
                js.extend(block_cls.Media.js)

        return js

    # Returns the JS files required by this page and its StreamField blocks.
    @property
    def media(self):
        return sorted(set(self.page_js + self.streamfield_js))

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        return self.social_sharing_image

    @property
    def post_preview_cache_key(self):
        return 'post_preview_{}'.format(self.id)


class COSMEPageCategory(Orderable):
    page = ParentalKey(COSMEPage, related_name='categories')
    name = models.CharField(max_length=255, choices=ref.categories)

    panels = [
        FieldPanel('name'),
    ]


from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from datetime import date


class AbstractFilterPage(COSMEPage):
    header = StreamField([
        ('article_subheader', blocks.RichTextBlock(icon='form')),
        ('text_introduction', molecules.TextIntroduction()),
        ('item_introduction', organisms.ItemIntroduction()),
    ], blank=True)
    preview_title = models.CharField(max_length=255, null=True, blank=True)
    preview_subheading = models.CharField(
        max_length=255, null=True, blank=True)
    preview_description = RichTextField(null=True, blank=True)
    secondary_link_url = models.CharField(
        max_length=500, null=True, blank=True)
    secondary_link_text = models.CharField(
        max_length=255, null=True, blank=True)
    preview_image = models.ForeignKey(
        'v1.COSMEImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date_published = models.DateField(default=date.today)
    date_filed = models.DateField(null=True, blank=True)
    comments_close_by = models.DateField(null=True, blank=True)

    # Configuration tab panels
    settings_panels = [
        MultiFieldPanel(COSMEPage.promote_panels, 'Settings'),
        InlinePanel('categories', label="Categories", max_num=2),
        FieldPanel('tags', 'Tags'),
        MultiFieldPanel([
            FieldPanel('preview_title', classname="full"),
            FieldPanel('preview_subheading', classname="full"),
            FieldPanel('preview_description', classname="full"),
            FieldPanel('secondary_link_url', classname="full"),
            FieldPanel('secondary_link_text', classname="full"),
            ImageChooserPanel('preview_image'),
        ], heading='Page Preview Fields', classname='collapsible'),
        FieldPanel('authors', 'Authors'),
        MultiFieldPanel([
            FieldPanel('date_published'),
            FieldPanel('date_filed'),
            FieldPanel('comments_close_by'),
        ], 'Relevant Dates', classname='collapsible'),
        MultiFieldPanel(Page.settings_panels, 'Scheduled Publishing'),
    ]

    # This page class cannot be created.
    is_creatable = False

    objects = COSMEPageManager()

    @classmethod
    def generate_edit_handler(self, content_panel):
        content_panels = [
            StreamFieldPanel('header'),
            content_panel,
        ]
        return TabbedInterface([
            ObjectList(self.content_panels + content_panels,
                       heading='General Content'),
            ObjectList(COSMEPage.sidefoot_panels, heading='Sidebar'),
            ObjectList(self.settings_panels, heading='Configuration'),
        ])

    # Returns an image for the page's meta Open Graph tag
    @property
    def meta_image(self):
        parent_meta = super(AbstractFilterPage, self).meta_image
        return parent_meta or self.preview_image
