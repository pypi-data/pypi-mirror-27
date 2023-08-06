# -*- coding: utf-8 -*-

# built-in
from collections import namedtuple
from functools import update_wrapper
# django
from django.views.generic import View
# project
from .exceptions import StatusCodeError, SubValidationError
from .parsers import Default as _DefaultParser


__all__ = ['rule', 'ViewBase']


_fields = ['d', 'p', 'prev', 'c', 'postv', 'prer', 'postr', 'r']
_Rule = namedtuple('Rule', _fields)


def _get_value(v, kwargs):
    if type(v) is str:
        return _get_value(kwargs[v], kwargs)
    else:
        return v


def rule(**kwargs):
    """Factory for _Rule objects

    * Any kwarg can contain str which point where function can get value
        for kwarg.
    * Some kwargs can contain None.

    Example:
        rule(
            d=[login_required, csrf_exempt],    # decorators
            prev=SomeDjangoForm,    # pre-validator
            c=some_controller,      # controller
            postv=None,             # post-validator
            # ^ here post-validator is missed
            prer='postr',           # renderer for pre-validator errors
            # ^ here `prer` point to `postr`
            postr='r',              # renderer for post-validator errors
            r=djburger.r.JSON(),    # renderer
        )

    Kwargs:
        - d (list): list of decorators
        - p (callable): parser. Parse request body.
            `djburger.p.Default` by default.
        - prev: pre-validator. Validate and clean user params
        - c (callable): controller
        - postv: post-validator. Validate and clean response
        - prer (callable): renderer for pre-validator errors
        - postr (callable): renderer for post-validator errors
        - r (callable): renderer for successfull response
    """
    # check required kwargs
    if 'c' not in kwargs:
        TypeError('Controller is required')
    if 'r' not in kwargs:
        TypeError('Renderer is required')
    # set default parser
    if 'p' not in kwargs:
        kwargs['p'] = _DefaultParser()
    # set 'r' as default for error-renderers
    for f in ('prer', 'postr'):
        if f not in kwargs:
            kwargs[f] = 'r'
    # set None as default for others
    for f in ('d', 'prev', 'postv'):
        if f not in kwargs:
            kwargs[f] = None

    for k, v in kwargs.items():
        kwargs[k] = _get_value(v, kwargs)
    return _Rule(**kwargs)


class ViewBase(View):
    """Base views for DjBurger usage
    """
    rules = None
    rule = None
    default_rule = None

    def dispatch(self, request, **kwargs):
        """Entrypoint for view

        1. Select rule from rules.
        2. Decorate view
        3. Call `validate` method.

        Args:
            - request (Request): Request object.
            - \**kwargs: kwargs from urls.py.

        Returns:
            - HttpResponse: django http response
        """
        self.method = request.method.lower()
        if self.rules and self.method in self.rules:
            self.rule = self.rules[self.method]
        elif self.default_rule:
            self.rule = self.default_rule
        else:
            raise NotImplementedError('Please, set rule or rules attr')

        base = self.validate_request

        # decorators
        if self.rule.d:
            for decorator in self.rule.d:
                base = decorator(base)
            # take possible attributes set by decorators like csrf_exempt
            base = update_wrapper(base, self.validate, assigned=())

        return base(request, **kwargs)

    def get_data(self, request):
        return self.rule.p(request)

    # pre-validator
    def validate_request(self, request, **kwargs):
        """
        1. Call `request_valid` method if validation is successfull or missed.
        2. Call `request_invalid` method otherwise.

        Args:
            - request (Request): Request object
            - \**kwargs: kwargs from urls.py.

        Returns:
            - HttpResponse: django http response
        """
        # data
        data = self.get_data(request)

        # no validator
        if not self.rule.prev:
            return self.request_valid(data, **kwargs)

        # validate
        validator = self.rule.prev(**self.get_validator_kwargs(data))
        try:
            is_valid = validator.is_valid()
        except StatusCodeError as e:
            is_valid = False
            status_code = e.status_code
        else:
            status_code = None
        if is_valid:
            return self.request_valid(validator.cleaned_data, **kwargs)
        else:
            return self.request_invalid(validator, status_code=status_code)

    # pre-validation error renderer
    def request_invalid(self, validator, status_code):
        """Return result of prer (renderer for pre-validator errors)

        Args:
            - validator: validator object with `errors` attr.
            - status_cdoe: status code for HTTP-response

        Returns:
            - HttpResponse: django http response
        """
        return self.rule.prer(
            request=self.request,
            validator=validator,
            status_code=status_code,
        )

    # controller
    def request_valid(self, data, **kwargs):
        """Call controller.

        Get response from controller and return result of validate_response
        method.

        Args:
            - data: cleaned and validated data from user.
            - \**kwargs: kwargs from urls.py.

        Returns:
            - HttpResponse: django http response
        """
        # get response from controller
        try:
            response = self.rule.c(self.request, data, **kwargs)
        except SubValidationError as e:
            validator = e.args[0]
            return self.subvalidation_invalid(validator)
        return self.validate_response(response)

    # post-validator
    def validate_response(self, response):
        """Validate response by postv (post-validator)

        1. Return make_response method result if post-validator is missed.
        2. Validate data by post-validator otherwise and call...
            * response_valid if validation is passed
            * or response_invalid otherwise.

        Args:
            - response: data from controller

        Returns:
            - HttpResponse: django http response
        """
        # no post-validator
        if not self.rule.postv:
            return self.make_response(data=response)

        # post-validation
        params = self.get_validator_kwargs(response)
        validator = self.rule.postv(**params)
        try:
            is_valid = validator.is_valid()
        except StatusCodeError as e:
            is_valid = False
            status_code = e.status_code
        else:
            status_code = None
        if is_valid:
            return self.response_valid(validator)
        else:
            return self.response_invalid(validator, status_code=status_code)

    # renderer for errors in subcontroller's validator
    def subvalidation_invalid(self, validator, status_code=200):
        return self.response_invalid(validator, status_code)

    # post-validation error renderer
    def response_invalid(self, validator, status_code):
        """Return result of postr (renderer for post-validation errors).

        Args:
            - validator: post-validator object with `errors` attr.
            - status_cdoe: status code for HTTP-response

        Returns:
            - HttpResponse: django http response
        """
        return self.rule.postr(
            request=self.request,
            validator=validator,
            status_code=status_code,
        )

    # successfull response renderer
    def response_valid(self, validator):
        """Return result of make_response.

        This method calls only if postv is not None.

        Args:
            - validator: validator object with `cleaned_data` attr.

        Returns:
            - HttpResponse: django http response
        """
        return self.make_response(validator.cleaned_data)

    def make_response(self, data):
        """Make response by renderer

        Args:
            - data: validated and cleaned data from controller

        Returns:
            - HttpResponse: django http response
        """
        return self.rule.r(request=self.request, data=data)

    # send request and data into validator
    def get_validator_kwargs(self, data):
        """Get kwargs for validators

        Args:
            - data: source data from user.

        Returns:
            - dict: kwargs for (post)validator
        """
        try:
            kwargs = super(ViewBase, self).get_form_kwargs()
        except AttributeError:
            kwargs = {}
        kwargs['request'] = self.request
        kwargs['data'] = data
        return kwargs
