import logging

logger = logging.getLogger(__name__)


class ErrorMiddleware(object):
    @staticmethod
    def process_exception(request, exception):
        logger.exception('Uncaught exception', extra={
            'request': request,
            'exception': exception,
        })
        return None
