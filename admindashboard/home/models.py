import datetime

from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.api.fields import ImageRenditionField


# ─── Generic page types ───────────────────────────────────────────────────────
#
#  These three types are enough to manage any website:
#
#  GenericHomePage          ← one per website, controls H1 + meta description
#      └── GenericSectionPage   ← one per section (blogs, services, news, …)
#              └── GenericDetailPage    ← one per item (post, service, project, …)


class GenericHomePage(Page):
    """
    Root page for any website managed by this dashboard.
    Controls the H1 heading and meta description of the site home page,
    plus any intro body content the frontend wants to pull.
    """

    h1_title = models.CharField(
        max_length=255, blank=True,
        help_text="Main H1 heading shown on the homepage",
    )
    meta_description = models.TextField(
        blank=True,
        help_text="Meta description for search engines (150–160 chars recommended)",
    )
    body = StreamField([
        ('rich_text',  blocks.RichTextBlock()),
        ('embed_html', blocks.RawHTMLBlock(label='Embed HTML')),
    ], use_json_field=True, blank=True,
       help_text="Optional intro content the frontend can display on the home page")

    subpage_types = ['home.GenericSectionPage']

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('h1_title'),
            FieldPanel('meta_description'),
        ], heading='SEO'),
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('h1_title'),
        APIField('meta_description'),
        APIField('body'),
    ]

    class Meta:
        verbose_name = "Home Page"


class GenericSectionPage(Page):
    """
    A section/listing page (e.g. /blogs/, /services/, /news/).
    Has its own H1 + meta description + optional body content.
    Can hold detail pages or nest further section pages.
    """

    h1_title = models.CharField(
        max_length=255, blank=True,
        help_text="Heading shown at the top of this section (e.g. 'Our Services')",
    )
    meta_description = models.TextField(
        blank=True,
        help_text="Meta description for search engines",
    )
    body = StreamField([
        ('rich_text',  blocks.RichTextBlock()),
        ('embed_html', blocks.RawHTMLBlock(label='Embed HTML')),
    ], use_json_field=True, blank=True,
       help_text="Optional content shown on the listing page (intro text, embedded components, etc.)")

    parent_page_types = ['home.GenericHomePage', 'home.GenericSectionPage']
    subpage_types     = ['home.GenericSectionPage', 'home.GenericDetailPage']

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('h1_title'),
            FieldPanel('meta_description'),
        ], heading='SEO'),
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('h1_title'),
        APIField('meta_description'),
        APIField('body'),
    ]

    class Meta:
        verbose_name = "Section Page"


class GenericDetailPage(Page):
    """
    A detail/content page (blog post, service, project, news article, …).
    The frontend decides how to display the data — the dashboard just stores it.
    """

    meta_description = models.TextField(
        blank=True,
        help_text="Meta description for search engines",
    )
    date = models.DateField(
        "Date", default=datetime.date.today, null=True, blank=True,
        help_text="Publication or project date (leave blank if not applicable)",
    )
    excerpt = models.TextField(
        blank=True,
        help_text="Short summary shown on listing cards (2–3 sentences)",
    )
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Main image shown on listing cards and at the top of the detail page",
    )
    body = StreamField([
        ('rich_text',  blocks.RichTextBlock()),
        ('image',      ImageChooserBlock()),
        ('embed_html', blocks.RawHTMLBlock(label='Embed HTML')),
    ], use_json_field=True, blank=True,
       help_text="Full page content — mix rich text, images, and embedded HTML freely")

    parent_page_types = ['home.GenericSectionPage']
    subpage_types     = []

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('meta_description'),
            FieldPanel('date'),
            FieldPanel('excerpt'),
            FieldPanel('cover_image'),
        ], heading='Page Info'),
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('meta_description'),
        APIField('date'),
        APIField('excerpt'),
        APIField('cover_image', serializer=ImageRenditionField('fill-800x450')),
        APIField('body'),
    ]

    class Meta:
        verbose_name = "Detail Page"
