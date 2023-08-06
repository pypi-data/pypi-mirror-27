# -*- coding: utf-8 -*-
"""
    tests.cubeswriters.conftest
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test configuration for CubesWriter
"""
import pytest
import csv
from itertools import islice
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from cubes import Workspace
from sqlalchemy.ext.declarative import declarative_base


@pytest.fixture
def base():
    return declarative_base()


@pytest.fixture(scope='session')
def engine():
    return create_engine('sqlite:///tests/test.db')


@pytest.yield_fixture(scope='function')
def session(engine, base):
    base.metadata.drop_all(engine)
    session = Session(bind=engine)

    yield session
    base.metadata.drop_all(engine)
    session.close()


@pytest.fixture
def test_data():
    with open('tests/data/hello_world_data.csv') as f:
        # islice to skip over the header and use our own
        return list(
            csv.DictReader(islice(f, 1, None),
                           fieldnames=[
                               'category',
                               'category_label',
                               'subcategory',
                               'subcategory_label',
                               'line_item',
                               'year',
                               'amount'
                           ]))


@pytest.fixture
def test_model_config_path():
    return 'tests/data/hello_world.json'


@pytest.fixture
def test_workspace(engine, test_model_config_path):
    workspace = Workspace()
    workspace.register_default_store('sql', url='sqlite:///tests/test.db')
    workspace.import_model(test_model_config_path)
    return workspace
