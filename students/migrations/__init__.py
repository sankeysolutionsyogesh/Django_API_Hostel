from django.db import migrations

def create_gender_constraint(apps, schema_editor):
    Student = apps.get_model('yourappname', 'Student')
    GENDER_CHOICES = ('M', 'F', 'O')

    # Create a constraint to ensure gender values are only from GENDER_CHOICES
    schema_editor.execute(
        f"ALTER TABLE {Student._meta.db_table} ADD CONSTRAINT gender_check "
        f"CHECK (gender IN {GENDER_CHOICES})"
    )

class Migration(migrations.Migration):

    dependencies = [
        ('yourappname', '000x_previous_migration'),
    ]

    operations = [
        migrations.RunSQL(
            sql='DROP CONSTRAINT IF EXISTS gender_check',
            reverse_sql='ALTER TABLE student DROP CONSTRAINT gender_check',
        ),
        migrations.RunPython(create_gender_constraint),
    ]
