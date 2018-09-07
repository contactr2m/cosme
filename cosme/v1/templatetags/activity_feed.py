from cosme.v1.models.base import AbstractFilterPage
from cosme.v1.util.categories import clean_categories


def get_latest_activities(activity_type, quantity=5):
    categories = clean_categories([activity_type])
    return (
        AbstractFilterPage.objects.live()
        .filter(categories__name__in=categories)
        .order_by("-date_published")[:quantity]
    )
