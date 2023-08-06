# -*- coding: utf-8 -*-


from openfisca_france_data.utils import (
    build_cerfa_fields_by_column_name)


def test_build_cerfa_fields_by_column_name():

    cerfa_fields_by_column_name_2006 = build_cerfa_fields_by_column_name(2006, [6, 7, 8])
    cerfa_fields_by_column_name_2009 = build_cerfa_fields_by_column_name(2006, [6, 7, 8])
    cerfa_fields_by_column_name_2012 = build_cerfa_fields_by_column_name(2012, [6, 7, 8])

    assert cerfa_fields_by_column_name_2006['f6ss'] == ['f6ss', 'f6st', 'f6su']
    assert cerfa_fields_by_column_name_2009['f6ss'] == ['f6ss', 'f6st', 'f6su']
    assert cerfa_fields_by_column_name_2012['f6ss'] == ['f6ss', 'f6st', 'f6su']

    assert cerfa_fields_by_column_name_2009.get('f7vw') is None
    assert cerfa_fields_by_column_name_2012.get('f7vw') == ['f7vw']
