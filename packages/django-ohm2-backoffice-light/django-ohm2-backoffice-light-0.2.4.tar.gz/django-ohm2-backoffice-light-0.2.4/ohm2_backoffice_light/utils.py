from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from ohm2_accounts_light import utils as ohm2_accounts_light_utils
from guardian.models import UserObjectPermission
from guardian.shortcuts import assign_perm
from . import models as ohm2_backoffice_light_models
from . import errors as ohm2_backoffice_light_errors
from . import settings
import os, time, random


random_string = "bcD8tYixjLe0gE9jW7V3NzlTepaM9m6q"



def create_staff(user, **kwargs):
	kwargs["user"] = user
	return h_utils.db_create(ohm2_backoffice_light_models.Staff, **kwargs)

def get_or_none_staff(**kwargs):
	return h_utils.db_get_or_none(ohm2_backoffice_light_models.Staff, **kwargs)
	
def get_staff(**kwargs):
	return h_utils.db_get(ohm2_backoffice_light_models.Staff, **kwargs)

def filter_staff(**kwargs):
	return h_utils.db_filter(ohm2_backoffice_light_models.Staff, **kwargs)

def q_staff(q):
	return h_utils.db_q(ohm2_backoffice_light_models.Staff, q)	

def get_staff_group():
	group = get_or_none_staff_group()
	if group:
		return group
	return create_staff_group()	

def get_or_none_staff_group():
	return h_utils.db_get_or_none(Group, name = "staff")

def create_staff_group():
	staff_group = h_utils.db_create(Group, name = "staff")
	return staff_group

def assign_permissions_to_staff_group(group, **kwargs):
	for perm in settings.STAFF_PERMISSIONS:
		assign_perm("ohm2_backoffice_light." + perm[0], group)
	return group	

def create_staff_user(username, email, password, **kwargs):
	user = ohm2_accounts_light_utils.create_user(username, email, password)

	try:
		user = h_utils.db_update(user, is_staff = True)
		staff = create_staff(user)
		
		staff_group = get_staff_group()

		staff_group = assign_permissions_to_staff_group(staff_group)

		user.groups.add(staff_group)		

	except Exception as e:
		h_utils.db_delete(user)
		raise RunException(**ohm2_backoffice_light_errors.FAILED_TO_CREATE_STAFF_USER)
	
	return user
