from ohm2_handlers_light import utils as h_utils
from ohm2_accounts_light import utils as ohm2_accounts_light_utils
from ohm2_backoffice_light.decorators import ohm2_backoffice_light_safe_request
from . import errors as ohm2_backoffice_light_api_v1_errors




@ohm2_backoffice_light_safe_request
def user_exist(request, params):
	p = h_utils.cleaned(params, (
							("string", "username", 0),
							("string", "email", 0),
						))

	
	username, email = p["username"], p["email"]
	
	if len(username) > 0:
		query = {"username" : username}

	elif len(email) > 0:
		query = {"email" : email}

	else:
		return {"error" : ohm2_backoffice_light_api_v1_errors.BOTH_CANT_BE_EMPTY}
	

	exist = ohm2_accounts_light_utils.user_exist(**query)
	

	res = {
		"error" : None,
		"ret" : exist,
	}
	return res



@ohm2_backoffice_light_safe_request
def is_password_secure(request, params):
	p = h_utils.cleaned(params, (
							("string", "username", 1),
							("string", "password", 1),
						))

	
	username, password = p["username"], p["password"]
	
	user = ohm2_accounts_light_utils.get_or_none_user(username = p["username"])
	secure = ohm2_accounts_light_utils.is_password_secure(password, user)
	
	#errors = ohm2_accounts_light_utils.validate_current_password(password, user)

	res = {
		"error" : None,
		"ret" : secure,
	}
	return res


