# Hand-edited: removed redundant RemoveField operations on models being deleted
# in the same migration. Those ops caused SQLite to attempt rebuilding tables
# without a primary key, producing a syntax error. DeleteModel drops the full
# table so the field removals are unnecessary on both SQLite and PostgreSQL.

import datetime
import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_civiliahomepage_primeshieldhomepage_and_more'),
        ('wagtailcore', '0097_baselogentry_uuid_action_timestamp_indexes'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        # ── Create new generic page types ─────────────────────────────────────
        migrations.CreateModel(
            name='GenericHomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('h1_title', models.CharField(blank=True, help_text='Main H1 heading shown on the homepage', max_length=255)),
                ('meta_description', models.TextField(blank=True, help_text='Meta description for search engines (150–160 chars recommended)')),
                ('body', wagtail.fields.StreamField([('rich_text', 0), ('embed_html', 1)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {}), 1: ('wagtail.blocks.RawHTMLBlock', (), {'label': 'Embed HTML'})}, help_text='Optional intro content the frontend can display on the home page')),
            ],
            options={'verbose_name': 'Home Page'},
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GenericSectionPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('h1_title', models.CharField(blank=True, help_text="Heading shown at the top of this section (e.g. 'Our Services')", max_length=255)),
                ('meta_description', models.TextField(blank=True, help_text='Meta description for search engines')),
                ('body', wagtail.fields.StreamField([('rich_text', 0), ('embed_html', 1)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {}), 1: ('wagtail.blocks.RawHTMLBlock', (), {'label': 'Embed HTML'})}, help_text='Optional content shown on the listing page (intro text, embedded components, etc.)')),
            ],
            options={'verbose_name': 'Section Page'},
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='GenericDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('meta_description', models.TextField(blank=True, help_text='Meta description for search engines')),
                ('date', models.DateField(blank=True, default=datetime.date.today, help_text='Publication or project date (leave blank if not applicable)', null=True, verbose_name='Date')),
                ('excerpt', models.TextField(blank=True, help_text='Short summary shown on listing cards (2–3 sentences)')),
                ('cover_image', models.ForeignKey(blank=True, help_text='Main image shown on listing cards and at the top of the detail page', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('body', wagtail.fields.StreamField([('rich_text', 0), ('image', 1), ('embed_html', 2)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {}), 1: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 2: ('wagtail.blocks.RawHTMLBlock', (), {'label': 'Embed HTML'})}, help_text='Full page content — mix rich text, images, and embedded HTML freely')),
            ],
            options={'verbose_name': 'Detail Page'},
            bases=('wagtailcore.page',),
        ),

        # ── Update body fields on kept models ─────────────────────────────────
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('hero', 3), ('about', 4), ('vision', 9), ('services', 12)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 1: ('wagtail.blocks.CharBlock', (), {'required': False}), 2: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 3: ('wagtail.blocks.StructBlock', [[('background_image', 0), ('brand', 1), ('title', 1), ('description', 2), ('highlight', 1), ('highlight_part2', 1)]], {}), 4: ('wagtail.blocks.StructBlock', [[('title', 1), ('description', 2)]], {}), 5: ('wagtail.blocks.CharBlock', (), {'required': True}), 6: ('wagtail.blocks.TextBlock', (), {'required': True}), 7: ('wagtail.blocks.StructBlock', [[('title', 5), ('text', 6), ('image_path', 5)]], {}), 8: ('wagtail.blocks.ListBlock', (7,), {}), 9: ('wagtail.blocks.StructBlock', [[('slides', 8)]], {}), 10: ('wagtail.blocks.StructBlock', [[('title', 5), ('desc', 6), ('image_path', 5)]], {}), 11: ('wagtail.blocks.ListBlock', (10,), {}), 12: ('wagtail.blocks.StructBlock', [[('services', 11)]], {})}),
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='body',
            field=wagtail.fields.StreamField([('rich_text', 0), ('hero', 4), ('embed_html', 5)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {}), 1: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 2: ('wagtail.blocks.CharBlock', (), {'required': False}), 3: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 4: ('wagtail.blocks.StructBlock', [[('background_image', 1), ('brand', 2), ('title', 2), ('description', 3), ('highlight', 2), ('highlight_part2', 2)]], {}), 5: ('wagtail.blocks.RawHTMLBlock', (), {'label': 'Embed HTML'})}),
        ),

        # ── Delete old site-specific models ───────────────────────────────────
        migrations.DeleteModel(name='BlogIndexPage'),
        migrations.DeleteModel(name='BlogPage'),
        migrations.DeleteModel(name='CiviliaHomePage'),
        migrations.DeleteModel(name='CiviliaNewsIndexPage'),
        migrations.DeleteModel(name='CiviliaNewsPage'),
        migrations.DeleteModel(name='PrimeShieldHomePage'),
        migrations.DeleteModel(name='PrimeShieldProjectPage'),
        migrations.DeleteModel(name='PrimeShieldProjectsIndexPage'),
        migrations.DeleteModel(name='PrimeShieldServicePage'),
        migrations.DeleteModel(name='PrimeShieldServicesIndexPage'),
    ]
