# -*- coding: utf-8 -*-
"""
    cubeswriter.parsers
    ~~~~~~~~~~~~~~~~~

    Tools to parse configs into SQLAlchemy models
"""
from cubes import read_model_metadata
from sqlalchemy.ext.declarative import declarative_base
from .modelers import model_cubes


def parse_models(f, Base=declarative_base()):
    models_metadata = read_model_metadata(f)
    cubes = models_metadata['cubes']
    dimensions = models_metadata['dimensions']
    types = models_metadata['types']
    return {
        'models': model_cubes(cubes, dimensions, types, Base),
        'base': Base
    }
