from django.db import migrations


def delete_legacy_pages(apps, schema_editor):
    HomePage = apps.get_model('home', 'HomePage')
    StandardPage = apps.get_model('home', 'StandardPage')
    # Deleting via the ORM cascades through page_ptr to wagtailcore_page,
    # which in turn cascades to any Site whose root_page pointed here.
    HomePage.objects.all().delete()
    StandardPage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_generichomepage_genericsectionpage_and_more'),
    ]

    operations = [
        migrations.RunPython(delete_legacy_pages, migrations.RunPython.noop),
        migrations.DeleteModel(name='HomePage'),
        migrations.DeleteModel(name='StandardPage'),
    ]
