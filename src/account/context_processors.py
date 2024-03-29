from __future__ import unicode_literals

from account.conf import settings
from common.models import Account


def account(request):
    ctx = {
        "account": Account.for_request(request),
        "ACCOUNT_OPEN_SIGNUP": settings.ACCOUNT_OPEN_SIGNUP,
    }
    return ctx
