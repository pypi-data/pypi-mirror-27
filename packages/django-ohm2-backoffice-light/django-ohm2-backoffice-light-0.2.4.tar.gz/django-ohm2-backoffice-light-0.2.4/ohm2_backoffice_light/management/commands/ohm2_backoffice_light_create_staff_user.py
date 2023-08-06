from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from ohm2_backoffice_light import utils as ohm2_backoffice_light_utils
import os

class Command(BaseCommand):
	
	def add_arguments(self, parser):
		parser.add_argument('-u', '--username')
		parser.add_argument('-e', '--email')
		parser.add_argument('-p', '--password')

	def handle(self, *args, **options):
		username = options["username"]
		email = options["email"]
		password = options["password"]
		
		ohm2_backoffice_light_utils.create_staff_user(username, email, password)
