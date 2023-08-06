# -*- coding: utf-8 -*-
"""
    cubeswriter.modelers
    ~~~~~~~~~~~~~~~~~~~~

    Tools to model SQLAlchemy
"""
from sqlalchemy import Column, Integer
from .helpers import (
    process_measures, process_dimensions,
    format_class_name, filter_dimensions_for_cube
)


def model_cube(cube, dimensions, types, base_class):
    fact = cube['name']
    measures = process_measures(cube['measures'], types)
    dimensions = process_dimensions(dimensions, types)
    return type(
        format_class_name(fact), (base_class,), {
            '__tablename__': cube['name'],
            'id': Column(Integer, primary_key=True),
            **{**measures, **dimensions}
        }
    )


def model_cubes(cubes, dimensions, types, base_class):
    return {format_class_name(cube['name']): model_cube(cube,
                                                        filter_dimensions_for_cube(cube, dimensions),
                                                        types, base_class)
            for cube in cubes}
