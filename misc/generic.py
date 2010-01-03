# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseGone

DEFAULT_PAGINATION = getattr(settings, 'PAGINATION_DEFAULT_PAGINATION', 10)

def redirect_by_name(request, name, **kwargs):
    if name is not None:
        return HttpResponsePermanentRedirect(reverse(name, args=tuple(kwargs.values())))
    else:
        return HttpResponseGone()


def dict_paginate(d):
    return dict(d, paginate_by = DEFAULT_PAGINATION)

def sort_list(request, *kargs, **kwargs):
    """
    Generic view for sorted lists
    Input values:
        sort_dict - dictionary key: value, where key - what user will see on URL, and value - actual ordering field
        default_sort - default key of sort_dict, for what will sorting by default
        generic_function - what call next to generate actuall list, by default - list_detail.object_list
        queryset_name - name of queryset witch need to be sorted
    Output values:
        sort_query - additional string for your links
        sort - value of current sorting
    """
    default_sort = kwargs.pop('default_sort', None)
    sort_dict = kwargs.pop('sort_dict', None)
    sort = request.GET.get('sort', default_sort)
    generic_function = kwargs.pop('generic_function', list_detail.object_list)
    queryset_name = kwargs.pop('queryset_name', 'queryset')
    if sort and sort_dict and queryset_name in kwargs:
        kwargs[queryset_name] = kwargs[queryset_name].order_by(sort_dict.get(sort, sort_dict[default_sort]))
    kwargs['extra_context'] = kwargs.get('extra_context', {})
    if sort != default_sort:
        kwargs['extra_context']['sort_query'] = 'sort=' + sort + '&'
    kwargs['extra_context']['sort'] = sort
    return generic_function(request, *kargs, **kwargs)
