import re
import logging
import azure.functions as func
from enum import Enum
from typing import Match, cast

from ..Exceptions.APIException import APIException
from ..Data.Enum.request_parts import RequestPart

class ValidatorTypes(Enum):
    REQUIRED = 'required'
    UNIQUE = 'uniques'
    NULLABLE = 'nullable'
    STRING  = 'string'
    BOOLEAN  = 'boolean'
    NUMERIC  = 'numeric'
    EMAIL  = 'email'

class RequestValidator():
    """ Validador de peticiones HTTP entrantes
    """

    request = None
    rules = None
    req_part = None
    is_valid = True
    errors = None
    error_code = 422
    session = None

    def __init__(self, rules: dict, req_part: str = 'body',):
        self.rules = rules
        self.req_part = req_part

    def validate(self, request: func.HttpRequest) -> bool:
        request_parts = [req.value for req in RequestPart]
        if self.rules is None:
            self.is_valid = True
            raise APIException("Validation not pass", status_code=self.error_code, payload=self.errors)
        if not self.req_part in request_parts:
            self.is_valid = False
            self.errors = {"error": f"The section is not in Request Part. [{str(', ').join(request_parts)}]", "field":"req_part"}
            self.error_code = 500
            raise APIException("Validation not pass", status_code=self.error_code, payload=self.errors)
        "Validate all the rules defined with the request"
        try:
            if self.req_part == RequestPart.BODY.value:
                self.request = cast(dict, request.get_json())
            if self.req_part == RequestPart.PARAM.value:
                self.request = cast(dict, request.route_params)
            if self.req_part == RequestPart.QUERY.value:
                self.request = cast(dict, request.params)
        except Exception:
            self.is_valid = False
            self.errors = {"error": "Can't proccess the request", "field": self.req_part}
            self.error_code = 422
            raise APIException("Can't proccess the request", status_code=self.error_code, payload=self.errors)

        self.is_valid = True
        for field in self.rules:
            is_none = False
            request_value = self.request.get(field)
            rule_params = self.rules.get(field)
            for rule_param in rule_params:
                if rule_param == 'nullable' and request_value is None:
                    is_none = True
                    break
                if rule_param == 'required' and not field in self.request:
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} is required", "field":field}
                    break
                elif (not is_none) and rule_param == 'string' and not isinstance(request_value, str):
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be text", "field":field}
                    break
                elif (not is_none) and rule_param == 'boolean' and not isinstance(request_value, bool):
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be true/false", "field":field}
                    break
                elif (not is_none) and rule_param == 'numeric' and not isinstance(request_value, (int, float)) and not request_value.isdigit():
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be a number", "field":field}
                    break
                elif (not is_none) and rule_param == 'email' and not self.is_mail(request_value):
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be a valid email", "field":field}
                    break
            if not self.is_valid:
                break

        if not self.is_valid:
            raise APIException("Can't proccess the request", status_code=self.error_code, payload=self.errors)
        
        return True

    def is_mail(self, text: str) -> Match or None:
        """ Verify if the input string has a email format

        Args:
            text (str): Email string

        Returns:
            Match or None: Indicates if there is a match according with email regex
        """
        email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        return re.search(email_regex, text)
    