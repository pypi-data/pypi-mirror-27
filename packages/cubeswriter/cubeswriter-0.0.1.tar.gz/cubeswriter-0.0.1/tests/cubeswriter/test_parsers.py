# -*- coding: utf-8 -*-
"""
    tests.cubeswriters.test_parsers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for CubeWriters' parsers
"""
import pytest
from cubeswriter import parse_models
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import func


@pytest.mark.integration
def test_parse_models(session, test_data,
                      test_model_config_path, test_workspace, base):
    # test parser parses and returns SQLAlchemy model
    models = parse_models(test_model_config_path, Base=base)
    assert 'base' in models and list(models['models']) == ['IrbdBalance']
    models['base'].metadata.create_all(session.get_bind())
    IrbdBalance = models['models']['IrbdBalance']
    assert type(IrbdBalance) == DeclarativeMeta

    # test ingestion works properly
    session.add_all(IrbdBalance(**x) for x in test_data)
    session.commit()
    record_count = session.query(IrbdBalance).count()
    assert record_count == len(test_data)

    # test cubes aggregates and ad-hoc aggregates match
    browser = test_workspace.browser("irbd_balance")
    result = browser.aggregate()

    assert result.summary["record_count"] == record_count
    amount_sum = session.query(func.sum(IrbdBalance.amount)).scalar()
    assert result.summary["amount_sum"] == amount_sum
    assert result.summary["double_amount_sum"] == amount_sum * 2
