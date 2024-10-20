# Create demo data
from django.core.management import BaseCommand

from website.demo import DemoData


class Command(BaseCommand):
    help = "Create demo users, groups and Neo4J data"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        DemoData.django_users_groups()
        DemoData.neo4j_demo_data()
