from __future__ import annotations

import logging
import re
from typing import IO, Generator, Iterator, List, Optional

from mysqldump_analyzer.entities import Column, ForeignKey, Index, Options, Table

logger = logging.getLogger(__name__)

CREATE_TABLE_REGEX = re.compile(r"^CREATE TABLE `(?P<table>[a-z0-9_]+)` \($")
COLUMN_REGEX = re.compile(
    r"^  `(?P<column>[a-zA-Z0-9_]+)` (?P<type>[a-z]+(\([0-9]+(,[0-9]+)*\))?)(?P<options>[^,]*),?$"
)
PRIMARY_KEY_REGEX = re.compile(r"^  PRIMARY KEY \(`(?P<column>[a-zA-Z0-9_]+)`\),?$")
FOREIGN_KEY_REGEX = re.compile(
    r"^  CONSTRAINT `(?P<foreign_key>[a-zA-Z0-9_]+)` FOREIGN KEY \(`(?P<column>[a-zA-Z0-9_]+)`\) REFERENCES `(?P<table>[a-z0-9_]+)` \(`(?P<target>[a-zA-Z0-9_]+)`\),?$"
)
INDEX_REGEX = re.compile(
    r"^  (?P<unique>(UNIQUE )?)KEY `(?P<index>[a-zA-Z0-9_]+)` \((?P<columns>`[a-zA-Z0-9_]+(`(\([0-9]+\))?,`[a-zA-Z0-9_]+)*`(\([0-9]+\))?)\),?$"
)


def parse(dump: IO[str]) -> List[Table]:
    """
    Parse a dump to get all the tables.

    :param dump: a dump
    :return: a list of tables of a dump
    """
    return list(_parse_all_tables(dump))


def _parse_all_tables(lines: Iterator[str]) -> Generator[Table, None, None]:
    """
    Parse a dump to get all the tables.

    :param lines: a line iterator containing the tables
    :return: a list of tables of a dump
    """
    table = None

    for line in lines:
        logger.debug("Reading line %s", line)
        match = CREATE_TABLE_REGEX.match(line)
        if match:
            table = Table(name=match.group("table"))
            logger.info("Found: %s", table)
            break

    if not table:
        logger.info("No other table found")
        return

    for line in lines:
        logger.debug("Reading line %s", line)

        try:
            column = _parse_column(line)
        except NotFound:
            pass
        else:
            logger.info("Found: %s", column)
            table.columns.append(column)
            continue

        try:
            index = _parse_index(line)
        except NotFound:
            pass
        else:
            logger.info("Found: %s", index)
            if index.primary_key:
                table.primary_key = index
            table.indexes.append(index)
            continue

        try:
            fk = _parse_foreign_key(line)
        except NotFound:
            pass
        else:
            logger.info("Found: %s", fk)
            if table:
                table.foreign_keys.append(fk)
            continue

        try:
            options = _parse_options(line)
        except NotFound:
            raise Exception

        if options.values:
            logger.info("Found: %s", options)
            if table:
                table.options = options

        break

    yield table

    yield from _parse_all_tables(lines)


def _parse_column(line: str) -> Optional[Column]:
    """
    Parse a column from a line.

    :param line: a line
    :return: the optional column
    """
    match = COLUMN_REGEX.match(line)
    if match:
        return Column(
            name=match.group("column"),
            sql_type=match.group("type"),
            options=match.group("options").strip(),
        )
    raise NotFound


def _parse_index(line: str) -> Optional[Index]:
    """
    Parse an index from a line.

    :param line: a line
    :return: the optional index
    """
    match = PRIMARY_KEY_REGEX.match(line)
    if match:
        return Index(
            name="primary key",
            columns=(match.group("column"),),
            unique=True,
            primary_key=True,
        )

    match = INDEX_REGEX.match(line)
    if match:
        return Index(
            name=match.group("index"),
            columns=tuple(match.group("columns").replace("`", "").split(",")),
            unique=len(match.group("unique")) > 1,
        )

    raise NotFound


def _parse_foreign_key(line: str) -> Optional[ForeignKey]:
    """
    Parse a foregin key from a line.

    :param line: a line
    :return: the optional foreignkey
    """
    match = FOREIGN_KEY_REGEX.match(line)
    if match:
        return ForeignKey(
            name=match.group("foreign_key"),
            column=match.group("column"),
            reference=(match.group("table"), match.group("target")),
        )
    raise NotFound


def _parse_options(line: str) -> Optional[Options]:
    """
    Parse the optionsfrom a line.

    :param line: a line
    :return: the optional options
    """
    if line.startswith(") "):
        options = re.sub(r"AUTO_INCREMENT=[0-9]+ ?", r"", line[2:])
        options = re.sub(r";$", r"", options)
        return Options(values=options)
    raise NotFound


class NotFound(Exception):
    """General NotFound exception."""

    pass
