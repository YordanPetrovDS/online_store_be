from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from common.exceptions import BusinessLogicException


def add_error_detail_to_list(error_details_dict: dict, errors_list: list):
    """Turn validation errors dict into FE-readable list"""
    for field, error_details in error_details_dict.items():
        for error_detail in error_details:
            err = {"field": field, "message": ""}
            # Add nested errors to the same list
            if isinstance(error_detail, dict):
                add_error_detail_to_list(error_detail, errors_list)
            else:
                err["message"] = str(error_detail)
            if err not in errors_list and err["message"]:
                errors_list.append(err)


def format_general_error_message(error_detail) -> dict:
    """Return error dict according to convention with FE"""
    return {"field": "non_field_errors", "message": str(error_detail)}


def custom_api_exception_handler(exception, context):
    """Set custom error messages format for validation errors"""
    response = exception_handler(exception, context)

    # If BusinessLogicException wasn't caught until now, show it to user as validation error
    if isinstance(exception, BusinessLogicException) and not response:
        return Response(
            [format_general_error_message(exception)],
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Make a list of error messages from validation errors
    elif isinstance(exception, ValidationError) and response is not None and response.data:
        if isinstance(response.data, dict):
            errors_list = []
            add_error_detail_to_list(response.data, errors_list)
            response.data = errors_list

        elif isinstance(response.data, list):
            errors_list = []
            for error in response.data:
                if isinstance(error, dict):
                    add_error_detail_to_list(error, errors_list)
                else:
                    # If we don't know the field names, mark them as non_field_errors
                    errors_list.append(format_general_error_message(error))
            response.data = errors_list
        return response

    # Reformat other errors to match validation errors format
    elif isinstance(exception, Http404):
        response.data = [format_general_error_message(_("Not found"))]
    elif response:
        response.data = [format_general_error_message(str(exception))]

    return response
