from django.conf import settings

from django_python3_ldap import utils


def genomix_search_filters(ldap_fields):
    """Filter LDAP for a given User group

    Args:
        ldap_fields (dict): Dict containing LDAP fields

    Returns:
        str: LDAP Search filter
    """
    ldap_fields["memberOf"] = settings.LDAP_AUTH_SEARCH_FILTER
    search_filters = utils.format_search_filters(ldap_fields)
    return search_filters
