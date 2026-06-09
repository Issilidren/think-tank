# Generated migration — adds owner and is_private to Project

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='owned_projects',
                to='voting.handle',
            ),
        ),
        migrations.AddField(
            model_name='project',
            name='is_private',
            field=models.BooleanField(
                default=False,
                help_text='Private projects only allow the owner to submit ideas.',
            ),
        ),
    ]
