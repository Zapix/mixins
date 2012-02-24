# -*- coding: utf-8 -*-
from django import http
from django.utils import simplejson as json


class JSONResponse(object):
    '''
    Gets method for JSONResponse
    '''
    def get_json_response(self, content, **kwargs):
        '''
            Construct an 'HttpResponse' object
        '''
        return  http.HttpResponse(content,
            content_type='application/json',
            **kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class JSONResponseMixin(JSONResponse):
    def render_to_response(self, context):
        '''
        Returns a JSON response containing 'context' as payload
        '''
        return self.get_json_response(self.convert_context_to_json(context))


class AJAXJSONResponseMixin(JSONResponse):
    def ajax_render(sekf, context):
        '''
        Return a JSON response containing 'context' as payload
        '''
        return self.get_json_response(self.convert_context_to_json(context))
