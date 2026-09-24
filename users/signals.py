import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from users.csv_utils import sync_users_to_csv
from users.models import User


@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def sync_user_csv(sender, **kwargs):
    """Keep the CSV mirror current for every User model write."""
    try:
        sync_users_to_csv()
    except PermissionError:
        logger = logging.getLogger(__name__)
        logger.warning("Could not update users.csv because it is locked.")
