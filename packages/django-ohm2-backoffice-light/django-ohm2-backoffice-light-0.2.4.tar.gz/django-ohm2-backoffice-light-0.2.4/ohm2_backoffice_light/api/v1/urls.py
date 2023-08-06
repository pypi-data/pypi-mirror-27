from django import VERSION as DJANGO_VERSION

if DJANGO_VERSION >= (2, 0):
	from django.urls import include, re_path as url
else:
	from django.conf.urls import include, url


from . import views

app_name = "ohm2_backoffice_light_api_v1"

urlpatterns = [
	url(r'^user-exist/$', views.user_exist, name = 'user_exist'),
	url(r'^is-password-secure/$', views.is_password_secure, name = 'is_password_secure'),
]