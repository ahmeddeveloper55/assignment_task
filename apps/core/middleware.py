import threading

import pytz
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.middleware.locale import LocaleMiddleware as DefaultLocaleMiddleware
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

thread_locals = threading.local()


def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user for
    JSON Web Token authentication. Inspects the token for the user_id,
    attempts to get that user from the DB & assigns the user on the
    request object. Otherwise it defaults to AnonymousUser.
    This will work with existing decorators like LoginRequired, whereas
    the standard restframework_jwt auth only works at the view level
    forcing all authenticated users to appear as AnonymousUser ;)
    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JWTAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except (Exception,):
        pass

    return user or AnonymousUser()


class LocaleMiddleware(DefaultLocaleMiddleware):
    """
    Parse a request and decide what translation object to install in the
    current thread context. This allows pages to be dynamically translated to
    the language the user desires (if the language is available).
    """

    def process_request(self, request):
        request.META['HTTP_ACCEPT_LANGUAGE'] = ''
        super(LocaleMiddleware, self).process_request(request)


class TimezoneMiddleware(MiddlewareMixin):
    """
    When support for time zones is enabled, Django stores datetime information in UTC in the database,
    uses time-zone-aware datetime objects internally,
    and translates them to the end user’s time zone in templates and forms.

    This is handy if your users live in more than one time zone and
    you want to display datetime information according to each user’s wall clock.

    Even if your website is available in only one time zone, it’s still good practice to store data in
    UTC in your database.
    The main reason is daylight saving time (DST).
    Many countries have a system of DST, where clocks are moved forward in spring and backward in autumn.
    If you’re working in local time, you’re likely to encounter errors twice a year, when the transitions happen.
    This probably doesn’t matter for your blog,
    but it’s a problem if you over bill or under bill your customers by one hour, twice a year, every year.
    The solution to this problem is to use UTC in the code and use local time only when interacting with end users.
    """

    def process_request(self, request):

        if request.user.is_anonymous:
            request.user = SimpleLazyObject(lambda: get_user_jwt(request))

        if request.user.is_authenticated:
            try:
                timezone.activate(pytz.timezone(request.user.profile.timezone))
            except (Exception,):
                timezone.deactivate()


class RequestMiddleware(MiddlewareMixin):
    """
    Middleware to set the request in the thread-local variable
    """

    def process_request(self, request):
        thread_locals.request = request


class ForceDefaultLanguagePrefixMiddleware:
    """
    Middleware to prepend the default language prefix to the request path internally
    if the URL path does not already start with a supported language code.
    This preserves the HTTP method, headers, and body without redirecting.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.supported_languages = [lang_code for lang_code, _ in settings.LANGUAGES]

    def __call__(self, request):
        path = request.path_info

        if not path.endswith('/'):
            path += '/'

        if not any(path.startswith(f'/{lang}/') for lang in self.supported_languages):
            # Prepend the default language prefix internally
            path = f'/{settings.LANGUAGE_CODE}{path}'

        request.path_info = path
        response = self.get_response(request)
        return response
