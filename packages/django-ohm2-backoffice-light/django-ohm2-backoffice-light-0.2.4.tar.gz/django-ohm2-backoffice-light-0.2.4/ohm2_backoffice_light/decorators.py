from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403
from ohm2_handlers_light.decorators import ohm2_handlers_light_safe_request
from . import settings

def ohm2_backoffice_light_safe_request(function):
	return ohm2_handlers_light_safe_request(function, "ohm2_backoffice_light")

def ohm2_backoffice_light_staff_views_or_403(func):

	@login_required(login_url = settings.LOGIN_URL)
	@permission_required_or_403("ohm2_backoffice_light." + settings.STAFF_PERMISSION_ENTER_VIEW[0], raise_exception = True)
	def wrapper(*args, **kwargs):
		return func(*args, **kwargs)

	return wrapper