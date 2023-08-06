import warnings

from wagtail.wagtailcore.models import Page, Site
from ..models.menuitems import MenuItem
from .deprecation import RemovedInWagtailMenus27Warning


def get_attrs_from_context(context):
    """
    Gets a bunch of useful things from the context/request and returns them as
    a tuple for use in most menu tags.
    """
    warning_msg = (
        "The 'get_attrs_from_context' method has been deprecated in favour of "
        "building this behaviour into the base Menu class"
    )
    warnings.warn(warning_msg, RemovedInWagtailMenus27Warning)
    request = context.get('request')
    site = get_site_from_request(request)
    wagtailmenus_vals = context.get('wagtailmenus_vals')
    current_page = wagtailmenus_vals.get('current_page')
    section_root = wagtailmenus_vals.get('section_root')
    ancestor_ids = wagtailmenus_vals.get('current_page_ancestor_ids')
    return (request, site, current_page, section_root, ancestor_ids)


def get_site_from_request(request, fallback_to_default=True):
    if getattr(request, 'site', None):
        return request.site
    if fallback_to_default:
        return Site.objects.filter(is_default_site=True).first()
    return None


def validate_supplied_values(tag, max_levels=None, use_specific=None,
                             parent_page=None, menuitem_or_page=None):
    if max_levels is not None:
        if max_levels not in (1, 2, 3, 4, 5):
            raise ValueError(
                "The `%s` tag expects `max_levels` to be an integer value "
                "between 1 and 5. Please review your template." % tag
            )
    if use_specific is not None:
        if use_specific not in (0, 1, 2, 3):
            raise ValueError(
                "The `%s` tag expects `use_specific` to be an integer value "
                "between 0 and 3. Please review your template." % tag
            )
    if parent_page is not None:
        if not isinstance(parent_page, Page):
            raise ValueError(
                "The `%s` tag expects `parent_page` to be a `Page` instance. "
                "A value of type `%s` was supplied." %
                (tag, parent_page.__class__)
            )
    if menuitem_or_page is not None:
        if not isinstance(menuitem_or_page, (Page, MenuItem)):
            raise ValueError(
                "The `%s` tag expects `menuitem_or_page` to be a `Page` or "
                "`MenuItem` instance. A value of type `%s` was supplied." %
                (tag, menuitem_or_page.__class__)
            )
