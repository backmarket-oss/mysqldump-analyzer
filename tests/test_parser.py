from mysqldump_analyzer.parser import parse


def test_parse(dump):
    result = parse(dump)
    assert len(result) == 2

    table1, table2 = result

    assert table1.name == "table_a"
    assert len(table1.columns) == 5
    assert len(table1.indexes) == 3
    assert len(table1.foreign_keys) == 1

    assert table2.name == "table_b"
    assert len(table2.columns) == 3
    assert len(table2.indexes) == 2
    assert len(table2.foreign_keys) == 1
