from django.conf import settings
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.models import Page, Site, PageViewRestriction


class MultiSitePagesAPIViewSet(PagesAPIViewSet):
    """
    Extends PagesAPIViewSet to serve pages from ALL Wagtail sites.

    The default viewset restricts results to the site that matches the
    request hostname:port.  In a headless multi-site setup the API lives
    at a different port (8000) than any frontend, so auto-detection always
    falls back to the default site and the other sites' pages are invisible.

    This viewset skips the auto-detected site filter.  You can still pass
    ?site=hostname[:port] to restrict to a specific site explicitly.
    """

    def get_base_queryset(self):
        request = self.request

        # Start with all live pages
        queryset = Page.objects.all().live()

        # Honour page view restrictions
        restricted_pages = [
            r.page
            for r in PageViewRestriction.objects.all().select_related("page")
            if not r.accept_request(request)
        ]
        for restricted_page in restricted_pages:
            queryset = queryset.not_descendant_of(restricted_page, inclusive=True)

        # Honour explicit ?site=hostname[:port] filter
        if "site" in request.GET:
            site_param = request.GET["site"]
            if ":" in site_param:
                hostname, port = site_param.split(":", 1)
                query = {"hostname": hostname, "port": port}
            else:
                query = {"hostname": site_param}
            try:
                site = Site.objects.get(**query)
            except Site.MultipleObjectsReturned:
                from wagtail.api.v2.filters import BadRequestError
                raise BadRequestError(
                    "Your query returned multiple sites. "
                    "Try adding a port number to your site filter."
                )
            except Site.DoesNotExist:
                return queryset.none()

            base_queryset = queryset
            queryset = base_queryset.descendant_of(site.root_page, inclusive=True)

            if getattr(settings, "WAGTAIL_I18N_ENABLED", False):
                for translation in site.root_page.get_translations():
                    queryset |= base_queryset.descendant_of(translation, inclusive=True)

        # No ?site= → return live pages from ALL sites (multi-site headless mode)
        # Type filtering (?type=home.CiviliaNewsPage etc.) in get_queryset() already
        # ensures only the right pages are returned.

        return queryset


api_router = WagtailAPIRouter("wagtailapi")
api_router.register_endpoint("pages", MultiSitePagesAPIViewSet)
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)
