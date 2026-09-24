from django.core.management.base import BaseCommand
from users.csv_utils import sync_users_to_csv, get_csv_path
from users.models import User

class Command(BaseCommand):
    help = 'Synchronize current User records from database into users.csv'

    def handle(self, *args, **options):
        csv_file = sync_users_to_csv()
        count = User.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Successfully synchronized {count} users to {csv_file}'))
