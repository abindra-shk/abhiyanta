# Generated by Django 4.1.3 on 2023-03-04 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_subject_faculty_remove_subject_semester_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upload_subjects',
            old_name='faculty',
            new_name='faculties',
        ),
    ]