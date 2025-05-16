# Generated manually to fix bucket schema

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name="Bucket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="Nome"),
                ),
                ("order", models.IntegerField(default=0, verbose_name="Ordem")),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
                "ordering": ["order", "name"],
            },
        ),
        migrations.AddField(
            model_name='task',
            name='bucket',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='tasks.bucket',
                verbose_name='Categoria',
            ),
        ),
    ]