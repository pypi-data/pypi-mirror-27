from django.utils.translation import ugettext as _

BASE_ERROR_CODE = 163648

BOTH_CANT_BE_EMPTY = {
	"code" : BASE_ERROR_CODE | 1,
	"message" : _("Both can't be empty"),
}
