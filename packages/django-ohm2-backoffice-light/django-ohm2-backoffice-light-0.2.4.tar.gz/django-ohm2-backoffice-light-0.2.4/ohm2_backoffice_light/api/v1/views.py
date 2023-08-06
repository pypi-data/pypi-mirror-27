from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from ohm2_handlers_light.parsers import get_as_or_get_default
from ohm2_backoffice_light.decorators import ohm2_backoffice_light_staff_views_or_403
from . import dispatcher




@api_view(['POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
@ohm2_backoffice_light_staff_views_or_403
def user_exist(request):
	"""
	Check if user exist

	__Inputs__:

		- username (string, optional)
		- email (string, optional)


	__Output__:

		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (boolean): true if exist or false if doesn't exist

	__Notes__:

		- At least one input must be present

	"""
	keys = (
		("username", "username", ""),
		("email", "email", ""),
	)
	res, error = dispatcher.user_exist(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error": error.regroup()})
	return JsonResponse(res)



@api_view(['POST'])
@authentication_classes((SessionAuthentication,))
@permission_classes((IsAuthenticated,))
@ohm2_backoffice_light_staff_views_or_403
def is_password_secure(request):
	"""
	Check if user's password is secure

	__Inputs__:

		- password (string, required)
		- username (string, optional)


	__Output__:

		- error (json-dict): describes the error (if known) with a code (integer) and a message (string).
		- ret (boolean): true if secure or false if not secure

	__Notes__:

		- At least one input must be present

	"""
	keys = (
		("username", "username", ""),
		("password", "password", ""),
	)
	res, error = dispatcher.is_password_secure(request, get_as_or_get_default(request.data, keys))
	if error:
		return JsonResponse({"error": error.regroup()})
	return JsonResponse(res)

