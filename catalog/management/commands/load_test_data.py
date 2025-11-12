from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
	help = "Clears existing products and categories, then loads fixtures"

	def handle(self, *args, **options):
		self.stdout.write(self.style.WARNING("Deleting existing data..."))
		Product.objects.all().delete()
		Category.objects.all().delete()

		self.stdout.write(self.style.WARNING("Loading fixtures..."))
		call_command('loaddata', 'catalog/fixtures/categories.json')
		call_command('loaddata', 'catalog/fixtures/products.json')
		self.stdout.write(self.style.SUCCESS("Test data loaded successfully."))

