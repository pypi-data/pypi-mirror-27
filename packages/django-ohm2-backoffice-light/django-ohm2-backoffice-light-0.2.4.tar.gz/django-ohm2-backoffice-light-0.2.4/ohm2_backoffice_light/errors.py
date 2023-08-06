from django.utils.translation import ugettext as _

BASE_ERROR_CODE = 91136

FAILED_TO_CREATE_STAFF_USER = {
	"code" : BASE_ERROR_CODE | 1, "message" : _("Failed to create staff user"),
}