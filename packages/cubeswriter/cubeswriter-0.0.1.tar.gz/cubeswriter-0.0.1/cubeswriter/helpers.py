# -*- coding: utf-8 -*-
"""
    cubeswriter.helpers
    ~~~~~~~~~~~~~~~~~~~

    utility functions for cubeswriter
"""
from sqlalchemy import Float, Column, String, Integer

TYPE_MAP = {
    'string': String,
    'float': Float,
    'integer': Integer
}


def process_measures(measures, types):
    return {
        m['name']: create_column(types[m['name']])
        for m in filter_measures(measures)}


def filter_measures(measures):
    return (m for m in measures if 'expression' not in m)


def filter_dimensions_for_cube(cube, dimensions):
    return (d for d in dimensions if d['name'] in cube['dimensions'])


def extract_dimensions(dimension_level):
    if 'levels' in dimension_level:
        return [d for dim in dimension_level['levels']
                for d in dim['attributes']]
    return [dimension_level['name']]


def process_dimensions(dimensions, types):
    return {
        x: create_column(types[x]) for dim in dimensions
        for x in extract_dimensions(dim)}


def create_column(type_str):
    return Column(TYPE_MAP[type_str])


def format_class_name(name):
    return ''.join(x.capitalize() for x in name.split('_'))
>
