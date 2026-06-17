import datetime

from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.api.fields import ImageRenditionField


class HeroBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(required=False, help_text="Background image for this hero section")
    brand = blocks.CharBlock(default="برايم شيلد |", required=False)
    title = blocks.CharBlock(default="خبرة هندسية في المقاولات العامة و خدمات العزل", required=False)
    description = blocks.RichTextBlock(default="شركة سعوديــــة رائــدة متخصصــة في حلــول العزل المائي والحراري...", required=False)
    highlight = blocks.CharBlock(default="نجمـــــع بيـــــن خبـــــــــــرة تتجـــــاوز 40 عامًـــــــــــا", required=False)
    highlight_part2 = blocks.CharBlock(default="وأكثـــر مــن 12 عامًــا من التخصص الدقيــق في أنظمة العزل الهندسـي", required=False)

    class Meta:
        icon = 'title'
        label = 'Hero Section'


class AboutBlock(blocks.StructBlock):
    title = blocks.CharBlock(default="من نحن", required=False)
    description = blocks.RichTextBlock(default="تأسست شركة برايم شيلد لتكون المحـور الأساسي الذي يلتقــي فيــــــــه الابتكــار الهندسي بالتميز الإنشائي...", required=False)

    class Meta:
        icon = 'user'
        label = 'About Section'


class VisionSlideBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=True)
    image_path = blocks.CharBlock(required=True, help_text="e.g. /assets/vision_result.webp")


class VisionBlock(blocks.StructBlock):
    slides = blocks.ListBlock(VisionSlideBlock())

    class Meta:
        icon = 'view'
        label = 'Vision Section'


class ServiceItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    desc = blocks.TextBlock(required=True)
    image_path = blocks.CharBlock(required=True, help_text="e.g. /assets/service-1_result.webp")


class ServicesBlock(blocks.StructBlock):
    services = blocks.ListBlock(ServiceItemBlock())

    class Meta:
        icon = 'cog'
        label = 'Services Section'


class HomePage(Page):
    body = StreamField([
        ('hero', HeroBlock()),
        ('about', AboutBlock()),
        ('vision', VisionBlock()),
        ('services', ServicesBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('body'),
    ]


class StandardPage(Page):
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('hero', HeroBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('body'),
    ]


# ─── Blog ────────────────────────────────────────────────────────────────────

class BlogIndexPage(Page):
    """Container page that holds all BlogPage children."""

    subpage_types = ['home.BlogPage']

    content_panels = Page.content_panels

    class Meta:
        verbose_name = "Blog Index Page"


class BlogPage(Page):
    date = models.DateField("Post date", default=datetime.date.today)
    author = models.CharField(max_length=255, blank=True)
    intro = models.TextField(
        blank=True,
        help_text="Short excerpt displayed on the blog listing page (2–3 sentences).",
    )
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Cover image shown in the blog card and at the top of the post.",
    )
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)

    parent_page_types = ['home.BlogIndexPage']

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('intro'),
        FieldPanel('cover_image'),
        FieldPanel('body'),
    ]

    api_fields = [
        APIField('date'),
        APIField('author'),
        APIField('intro'),
        APIField('cover_image', serializer=ImageRenditionField('fill-800x450')),
        APIField('body'),
    ]

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-date']


# ─── Civilia News ─────────────────────────────────────────────────────────────

class CiviliaNewsIndexPage(Page):
    """Container page that holds all CiviliaNewsPage children."""

    subpage_types = ['home.CiviliaNewsPage']
    content_panels = Page.content_panels

    class Meta:
        verbose_name = "Civilia News Index"


class CiviliaNewsPage(Page):
    date = models.DateField("Post date", default=datetime.date.today)
    excerpt = models.TextField(
        blank=True,
        help_text="Short description shown on the news listing cards.",
    )
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    content = RichTextField(blank=True)

    parent_page_types = ['home.CiviliaNewsIndexPage']

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('excerpt'),
        FieldPanel('cover_image'),
        FieldPanel('content'),
    ]

    api_fields = [
        APIField('date'),
        APIField('excerpt'),
        APIField('cover_image', serializer=ImageRenditionField('fill-800x450')),
        APIField('content'),
    ]

    class Meta:
        verbose_name = "Civilia News Post"
        verbose_name_plural = "Civilia News Posts"
        ordering = ['-date']
