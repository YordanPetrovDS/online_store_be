import datetime

from rest_framework import serializers


def validate_query_param(params: list, request, possible_choices: list = []) -> list:
    param_value_list = []
    for param in params:
        # Check if paramater exists
        try:
            param_value = request.query_params[param]
            param_value_list.append(param_value)
        except Exception:
            raise serializers.ValidationError(
                detail={"Error": f"There is missing filter field '{param}'"}
            )
        # Check if parameter values is empty
        if not param_value:
            raise serializers.ValidationError(detail={"Error": f"{param} is empty"})

        # Check if parameter values for date is in correct format
        if param.find("date") != -1:
            try:
                datetime.datetime.strptime(param_value, "%Y-%m-%d")
            except Exception:
                raise serializers.ValidationError(
                    detail={
                        "Error": f"Incorrect data format for param '{param}', should be YYYY-MM-DD"
                    }
                )

        # Check if parameter value for metric is one of the possible choices
        if param == "metric" and param_value not in possible_choices:
            error_message = (
                f"Incorrect value for filter field '{param}', "
                f"correct values are: {', '.join(possible_choices)}"
            )

            raise serializers.ValidationError(
                detail={"Error": error_message},
            )

    # Check if parameters are only three
    if (len(request.query_params) > 3 and "page" not in request.query_params) or (
        len(request.query_params) > 4 and "page" in request.query_params
    ):
        raise serializers.ValidationError(
            detail={
                "Error": f"The query params should be only the following ones - {','.join(params)}"
            }
        )

    return param_value_list
