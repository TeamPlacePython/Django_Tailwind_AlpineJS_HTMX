from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.members.models import Member


class Command(BaseCommand):
    """use this command to pass all members to pending
    'python manage.py reset_member_status --force'
    """

    help = "Reset status to 'pending' for all members with role='member'."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Exécute la commande quelle que soit la date.",
        )

    def handle(self, *args, **options):
        today = now().date()
        force_execution = options["force"]

        # Condition normale : 1er août
        if (today.month == 8 and today.day == 1) or force_execution:
            members = Member.objects.filter(roles="member").exclude(
                status="pending"
            )
            updated_count = members.update(status="pending")

            self.stdout.write(
                self.style.SUCCESS(
                    f"{updated_count} membres mis à jour (status='pending') ✔️"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Utilisez --force pour exécuter à toute les dates."
                )
            )
