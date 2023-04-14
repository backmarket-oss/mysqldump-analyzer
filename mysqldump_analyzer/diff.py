import logging
from collections import defaultdict
from typing import IO, Any, Dict, List, Set

from mysqldump_analyzer.entities import Table
from mysqldump_analyzer.parser import parse

logger = logging.getLogger(__name__)


def diff_dumps(**dumps: IO[str]) -> Dict[str, Any]:
    """
    Parse the dumps and create difference reports.

    :param dumps: all the dumps to differenciat
    :return: all the difference reports in the dumps
    """
    dbs = dict()
    for key, dump in dumps.items():
        dbs[key] = parse(dump)
    return diff_dbs(**dbs)


def diff_dbs(**dbs: List[Table]) -> Dict[str, Any]:
    """
    Differenciate a list of tables of a dump.

    :param dbs: a list of the tables
    :return: all the table's difference report in the dumps
    """
    result: Dict[str, Any] = defaultdict(dict)

    tables_names = set.union(*[{table.name for db in dbs.values() for table in db}])
    for table_name in tables_names:
        tables = dict()
        summary = dict()
        for key, db in dbs.items():
            for table in db:
                if table_name == table.name:
                    summary[key] = str(table)
                    tables[key] = table
                    break
            else:
                summary[key] = "missing"
        if len(set(summary.values())) > 1:
            result[table_name]["summary"] = summary
        if len(tables) > 1:
            result[table_name].update(diff_tables(**tables))
    return dict(result)


def diff_tables(**tables: Table) -> Dict[str, Any]:
    """
    Differenciate a table of a dump.

    :param tables: a table
    :return: the table's difference report in the dumps
    """
    result: Dict[str, Any] = defaultdict(dict)

    tables_names = {table.name for table in tables.values()}
    if len(tables_names) != 1:
        result["names"] = {key: table.name for key, table in tables.items()}

    for attr_name in ["columns", "indexes", "foreign_keys"]:
        elements_names = set.union(
            *[{element.name for element in getattr(table, attr_name)} for table in tables.values()]
        )
        logger.info("Comparing %s: %s", attr_name, elements_names)
        for element_name in elements_names:
            descriptions = dict()
            for key, table in tables.items():
                for element in getattr(table, attr_name):
                    if element_name == element.name:
                        descriptions[key] = str(element)
                        break
                else:
                    descriptions[key] = "missing"
            if len(set(descriptions.values())) > 1:
                result[attr_name][element_name] = descriptions

    descriptions = dict()
    for key, table in tables.items():
        if table.options:
            descriptions[key] = str(table.options)
        else:
            descriptions[key] = "missing"
        if len(set(descriptions.values())) > 1:
            result["options"] = descriptions

    return dict(result)
