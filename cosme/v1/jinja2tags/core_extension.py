from flags.template_functions import flag_disabled, flag_enabled
from jinja2.ext import Extension
from six.moves.urllib.parse import parse_qs, urlencode, urlparse
from django.core.signing import Signer
from django.urls import reverse
import re

from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe


def sign_url(url, secret=None):
    if secret:
        signer = Signer(secret, sep="||")
    else:
        signer = Signer(sep="||")

    url, signature = signer.sign(url).split("||")
    return (url, signature)


def signed_redirect(url):
    url, signature = sign_url(url)
    query_args = {"ext_url": url, "signature": signature}

    return "{0}?{1}".format(reverse("external-site"), urlencode(query_args))


def unsigned_redirect(url):
    query_args = {"ext_url": url}
    return "{0}?{1}".format(reverse("external-site"), urlencode(query_args))


register = template.Library()


SVG_REGEX = re.compile(
    r"^"  # start of string
    "\s*"  # any leading whitespace
    "<svg[^>]*>"  # opening <svg> tag with any attributes
    "(?!.*</svg>.*</svg>)"  # only allow one closing </svg> tag
    ".*</svg>"  # match anything and then the closing tag
    "\s*"  # any trailing whitespace
    "$",  # end of string
    re.DOTALL | re.IGNORECASE | re.MULTILINE,
)


@register.simple_tag()
def svg_icon(name):
    """Return SVG content given an icon name."""
    relative_path = "icons/{}.svg".format(name)
    static_filename = finders.find(relative_path)

    if not static_filename:
        raise ValueError("{} not found in staticfiles".format(relative_path))

    with open(static_filename, "r") as f:
        content = f.read()

        if not SVG_REGEX.match(content):
            raise ValueError("{} is not a valid SVG".format(static_filename))

        return mark_safe(content)


class CoreExtension(Extension):
    def __init__(self, environment):
        super(CoreExtension, self).__init__(environment)
        self.environment.globals.update(
            {
                "flag_enabled": flag_enabled,
                "flag_disabled": flag_disabled,
                "signed_redirect": signed_redirect,
                "unsigned_redirect": unsigned_redirect,
                "svg_icon": svg_icon,
            }
        )


filters = CoreExtension
