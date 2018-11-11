from time import time
import re
from six import text_type as str
from six.moves.urllib.parse import parse_qs, urlencode, urlparse

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import resolve

# from django.urls.base import resolve
from django.http import Http404, HttpResponseRedirect

from wagtail.core.blocks.stream_block import StreamValue

from bs4 import BeautifulSoup, NavigableString


NON_GOV_LINKS = re.compile(
    r"https?:\/\/(?:www\.)?(?![^\?]+gov)(?!(content\.)?localhost).*"
)
NON_CFPB_LINKS = re.compile(
    r"(https?:\/\/(?:www\.)?(?![^\?]*(cfpb|consumerfinance).gov)"
    r"(?!(content\.)?localhost).*)"
)
DOWNLOAD_LINKS = re.compile(r"(?i)(\.pdf|\.doc|\.docx|\.xls|\.xlsx|\.csv|\.zip)$")
LINK_ICON_CLASSES = "a-link a-link__icon"

LINK_ICON_TEXT_CLASSES = "a-link_text"


def get_unique_id(prefix="", suffix=""):
    index = hex(int(time() * 10000000))[2:]
    return prefix + str(index) + suffix


# These messages are manually mirrored on the
# Javascript side in error-messages-config.js

ERROR_MESSAGES = {
    "CHECKBOX_ERRORS": {"required": 'Please select at least one of the "%s" options.'},
    "DATE_ERRORS": {"invalid": "You have entered an invalid date."},
}


def instanceOfBrowseOrFilterablePages(page):
    from ..models import BrowsePage, BrowseFilterablePage

    pages = (BrowsePage, BrowseFilterablePage)
    return isinstance(page, pages)


# For use by Browse type pages to get the secondary navigation items
# TODO: Move into BrowsePage class once BrowseFilterablePage has been merged
# into BrowsePage
def get_secondary_nav_items(request, current_page):
    # If the parent page of the current page is a BrowsePage or a
    # BrowseFilterablePage, then use that as the top-level page for the
    # purposes of the navigation sidebar. Otherwise, treat the current page
    # as top-level.
    parent = current_page.get_parent().specific
    if instanceOfBrowseOrFilterablePages(parent):
        page = parent
    else:
        page = current_page

    # If there's no appropriate page version (e.g. not published for a sharing
    # request), then return no sidebar at all.
    if not page:
        return [], False

    # Return a boolean about whether or not the current page has Browse
    # children
    has_children = False

    # Handle the Newsroom page specially.
    # TODO: Remove this ASAP once Press Resources gets its own Wagtail page
    if page.slug == "newsroom":
        return (
            [
                {
                    "title": page.title,
                    "slug": page.slug,
                    "url": page.relative_url(request.site),
                    "children": [
                        {
                            "title": "Press Resources",
                            "slug": "press-resources",
                            "url": "/newsroom/press-resources/",
                        }
                    ],
                    "active": True,
                    "expanded": True,
                }
            ],
            True,
        )
    # END TODO

    if page.secondary_nav_exclude_sibling_pages:
        pages = [page]
    else:
        pages = filter(
            lambda p: instanceOfBrowseOrFilterablePages(p.specific),
            page.get_appropriate_siblings(),
        )

    nav_items = []
    for sibling in pages:
        if page.id == sibling.id:
            sibling = page
        else:
            sibling = sibling

        item_selected = current_page.pk == sibling.pk

        item = {
            "title": sibling.title,
            "slug": sibling.slug,
            "url": sibling.relative_url(request.site),
            "children": [],
            "active": item_selected,
            "expanded": item_selected,
        }

        if page.id == sibling.id:
            visible_children = filter(
                lambda c: (instanceOfBrowseOrFilterablePages(c) and (c.live)),
                sibling.get_children().specific(),
            )
            if len(visible_children):
                has_children = True
                for child in visible_children:
                    child_selected = current_page.pk == child.pk

                    if child_selected:
                        item["expanded"] = True

                    item["children"].append(
                        {
                            "title": child.title,
                            "slug": child.slug,
                            "url": child.relative_url(request.site),
                            "active": child_selected,
                        }
                    )

        nav_items.append(item)

    # Add `/process/` segment to OAH journey page nav urls.
    # TODO: Remove this when redirects for `/process/` urls
    # are added after 2018 homebuying campaign.
    # journey_urls = (
    #     '/owning-a-home/prepare',
    #     '/owning-a-home/explore',
    #     '/owning-a-home/compare',
    #     '/owning-a-home/close',
    #     '/owning-a-home/sources',
    # )
    # if current_page.relative_url(request.site).startswith(journey_urls):
    #     for item in nav_items:
    #         item['url'] = item['url'].replace(
    #             'owning-a-home', 'owning-a-home/process')
    #         for child in item['children']:
    #             child['url'] = child['url'].replace(
    #                 'owning-a-home', 'owning-a-home/process')
    # END TODO

    return nav_items, has_children


def valid_destination_for_request(request, url):

    view, args, kwargs = resolve(url)
    kwargs["request"] = request
    try:
        response = view(*args, **kwargs)
    except (Http404, TypeError):
        return False

    if isinstance(response, HttpResponseRedirect):
        # this indicates a permissions problem
        # (there may be a better way)
        if REDIRECT_FIELD_NAME + "=" in response.url:
            return False

    return True


def all_valid_destinations_for_request(request):
    possible_destinations = (("Wagtail", "/admin/"), ("Django admin", "/django-admin/"))
    valid_destinations = [
        pair
        for pair in possible_destinations
        if valid_destination_for_request(request, pair[1])
    ]

    return valid_destinations


def get_streamfields(page):
    """
    Retrieves the stream values on a page from its Streamfield
    """
    blocks_dict = {}
    for key, value in vars(page).items():
        if isinstance(value, StreamValue):
            blocks_dict.update({key: value})
    return blocks_dict


def extended_strftime(dt, format):
    """
    Extend strftime with additional patterns:
    _m for custom month abbreviations,
    _d for day values without leading zeros.
    """
    _MONTH_ABBREVIATIONS = [
        None,
        "Jan.",
        "Feb.",
        "Mar.",
        "Apr.",
        "May",
        "Jun.",
        "Jul.",
        "Aug.",
        "Sept.",
        "Oct.",
        "Nov.",
        "Dec.",
    ]

    format = format.replace("%_d", dt.strftime("%d").lstrip("0"))
    format = format.replace("%_m", _MONTH_ABBREVIATIONS[dt.month])
    return dt.strftime(format)


def is_image_tag(tag):
    for child in tag.children:
        if child.name in ["img", "svg"]:
            return True
    return False


def get_link_tags(soup):
    tags = []
    for a in soup.find_all("a", href=True):
        if not is_image_tag(a):
            tags.append(a)
    return tags


def add_link_markup(tag):
    # TODO: Fix this circular import.
    from cosme.v1.jinja2tags.core_extension import signed_redirect, svg_icon

    """Add necessary markup to the given link and return if modified.

    Add an external link icon if the input is not a CFPB (internal) link.
    Add an external link redirect if the input is not a gov link.
    Add a download icon if the input is a file.
    Otherwise (internal link that is not a file), return None.
    """
    icon = False

    if not tag.attrs.get("class", None):
        tag.attrs.update({"class": []})

    if tag["href"].startswith("/external-site/?"):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = "external-link"
        components = urlparse(tag["href"])
        arguments = parse_qs(components.query)
        if "ext_url" in arguments:
            external_url = arguments["ext_url"][0]
            # Add the redirect notice as well
            tag["href"] = signed_redirect(external_url)

    elif NON_CFPB_LINKS.match(tag["href"]):
        # Sets the icon to indicate you're leaving consumerfinance.gov
        icon = "external-link"
        if NON_GOV_LINKS.match(tag["href"]):
            # Add the redirect notice as well
            tag["href"] = signed_redirect(tag["href"])

    elif DOWNLOAD_LINKS.search(tag["href"]):
        # Sets the icon to indicate you're downloading a file
        icon = "download"

    if icon:
        tag.attrs["class"].append(LINK_ICON_CLASSES)
        # Wraps the link text in a span that provides the underline
        contents = tag.contents
        span = BeautifulSoup("", "html.parser").new_tag("span")
        span["class"] = LINK_ICON_TEXT_CLASSES
        span.contents = contents
        tag.contents = [span, NavigableString(" ")]
        # Appends the SVG icon
        tag.contents.append(BeautifulSoup(svg_icon(icon), "html.parser"))
        return str(tag)

    return None
