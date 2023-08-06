from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LocaleMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        lang = request.GET.get('lang', 'en')
        translation.activate(lang)
