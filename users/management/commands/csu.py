from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.ru',
            first_name='admin_ad',
            last_name='admin_admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('admin')
        user.save()
