from django.core.management.base import BaseCommand
from voting.models import Project


class Command(BaseCommand):
    help = 'Create the default Project (id=1) if it does not exist'

    def handle(self, *args, **options):
        project, created = Project.objects.get_or_create(
            pk=1,
            defaults={'title': 'Game Idea Think Tank — Dakota Cohort'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))
        else:
            self.stdout.write(f'Project already exists: {project.title}')
