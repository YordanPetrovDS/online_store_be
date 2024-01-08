import datetime
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError as CoreValidationError
from django.core.validators import FileExtensionValidator
from rest_framework.exceptions import ValidationError


def image_validator(file):
    file_validator(file, settings.IMAGE_MAX_MB, settings.IMAGE_VALID_EXTENSIONS)


def video_validator(file):
    file_validator(file, settings.VIDEO_MAX_MB, settings.VIDEO_VALID_EXTENSIONS)


def document_validator(file):
    file_validator(file, settings.DOCUMENT_MAX_MB, settings.DOCUMENT_VALID_EXTENSIONS)


def dowload_file_validator(file):
    file_validator(file, settings.DOWNLOAD_FILE_MAX_MB, settings.DOWNLOAD_FILE_VALID_EXTENSIONS)


def file_validator(file, max_size_mb: int, valid_extensions: List[str]):
    max_size_bytes = max_size_mb * 1024**2

    # Check file format
    FileExtensionValidator(allowed_extensions=valid_extensions)(file)

    # Check file size
    if file.size > max_size_bytes:
        raise ValidationError(f"Maximum allowed file size is {max_size_mb}MB.")


def validate_no_spaces(value):
    if " " in value:
        raise CoreValidationError("No spaces allowed")


def validate_query_param(params: list, request, possible_choices: list = []) -> list:
    param_value_list = []
    for param in params:
        # Check if paramater exists
        try:
            param_value = request.query_params[param]
            param_value_list.append(param_value)
        except Exception:
            raise ValidationError(f"There is missing filter field '{param}'")
        # Check if parameter values is empty
        if not param_value:
            raise ValidationError(f"{param} is empty")

        # Check if parameter values for date is in correct format
        if param.find("date") != -1:
            try:
                datetime.datetime.strptime(param_value, "%Y-%m-%d")
            except Exception:
                raise ValidationError(f"Incorrect data format for param '{param}', should be YYYY-MM-DD")

        # Check if parameter value for metric is one of the possible choices
        if param == "metric" and param_value not in possible_choices:
            error_message = (
                f"Incorrect value for filter field '{param}', " f"correct values are: {', '.join(possible_choices)}"
            )

            raise ValidationError(error_message)

    # Check if parameters are only three
    if (len(request.query_params) > 3 and "page" not in request.query_params) or (
        len(request.query_params) > 4 and "page" in request.query_params
    ):
        raise ValidationError(f"The query params should be only the following ones - {','.join(params)}")

    return param_value_list
