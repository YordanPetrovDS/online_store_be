from rest_framework import serializers


def validate_query_param(param: str, request, possible_choices: list = []):
    # Check if paramater exists
    try:
        param_value: str = request.query_params[param]
    except Exception:
        raise serializers.ValidationError(
            detail={"Error": f"There is missing filter field '{param}'"}
        )

    if not param_value:
        raise serializers.ValidationError(detail={"Error": f"{param} is empty"})

    # Check if parameter value is one of the possible choices
    if possible_choices and param_value not in possible_choices:
        raise serializers.ValidationError(
            detail={
                "Error": f"Incorrect value for filter field '{param}', correct values are: {', '.join(possible_choices)}"
            },
        )

    return param_value
