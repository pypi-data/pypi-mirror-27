"""
Django REST framework handles the following exceptions, and automatically generates error responses:
  - Subclasses of APIException raised inside REST framework,
  - Django's Http404 exception,
  - and Django's PermissionDenied exception.

More info: http://www.django-rest-framework.org/api-guide/exceptions/

We capture them here, and reformat responses to our desired style.
"""
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

from django_on_chain.exceptions import ServiceError


def reformat_error_handler(e, context):
    response = exception_handler(e, context)  # Call default exception handler to get the standard error response

    reformat_errors = getattr(context.get('view', object()), 'reformat_errors', False)

    if reformat_errors:
        # Order is important
        return reformat_service_error(e) or \
            reformat_drf_validation_error(e) or \
            reformat_drf_api_exception(e) or \
            reformat_django_http_404(e) or \
            reformat_django_permission_denied(e) or \
            response

    return response


def reformat_service_error(e):
    if isinstance(e, ServiceError):
        return Response({
            'type': e.type,
            'message': e.message,
        }, status=e.suggested_http_status or status.HTTP_500_INTERNAL_SERVER_ERROR)

    return None


def reformat_drf_validation_error(e):
    if isinstance(e, serializers.ValidationError):
        return Response({
            'type': 'bad_request',
            'message': _('Invalid request: {}').format(e.detail),
        }, status=status.HTTP_400_BAD_REQUEST)

    return None


def reformat_drf_api_exception(e):
    if isinstance(e, APIException):
        return Response({
            'type': e.default_code,
            'message': force_text(e.default_detail),
        }, status=e.status_code)

    return None


def reformat_django_http_404(e):
    if isinstance(e, Http404):
        return Response({
            'type': 'not_found',
            'message': _('Resource was not found'),
        }, status=status.HTTP_404_NOT_FOUND)

    return None


def reformat_django_permission_denied(e):
    if isinstance(e, PermissionDenied):
        return Response({
            'type': 'access_forbidden',
            'message': _('You do not have permission to perform the action requested'),
        }, status=status.HTTP_403_FORBIDDEN)
    return None
