from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class Column:
    name: str
    sql_type: str
    options: str

    def __str__(self) -> str:
        return f"column `{self.name}` {self.sql_type} {self.options.lower()}"


@dataclass(frozen=True)
class Index:
    name: str
    columns: Tuple[str, ...]
    unique: bool = False
    primary_key: bool = False

    def __post_init__(self) -> None:
        if self.primary_key:
            if not self.unique:
                raise ValueError("a primary key is a unique constraint")
            if self.name != "primary key":
                raise ValueError("a primary key has no name")

    def __str__(self) -> str:
        columns = ", ".join(f"`{col}`" for col in self.columns)
        if self.primary_key:
            return f"primary key on ({columns})"
        if self.unique:
            return f"unique index `{self.name}` on ({columns})"
        return f"index `{self.name}` on ({columns})"

    def covers(self, other: Index) -> bool:
        if other.primary_key:
            return False
        if other.unique:
            return self.unique and other.columns == self.columns
        if len(other.columns) > len(self.columns):
            return False
        return other.columns == self.columns[: len(other.columns)]


@dataclass(frozen=True)
class ForeignKey:
    name: str
    column: str
    reference: Tuple[str, str]

    def __str__(self) -> str:
        table, column = self.reference
        return f"foreign key `{self.name}` reference to `{table}`.`{column}`"


@dataclass(frozen=True)
class Options:
    values: str

    def __str__(self) -> str:
        return f"options {self.values}"

    def __bool__(self) -> bool:
        return bool(self.values)


@dataclass
class Table:
    name: str
    columns: List[Column] = field(default_factory=list)
    indexes: List[Index] = field(default_factory=list)
    foreign_keys: List[ForeignKey] = field(default_factory=list)
    primary_key: Optional[Index] = None
    options: Optional[Options] = None

    def __str__(self) -> str:
        nb_columns = len(self.columns)
        return f"table `{self.name}` with {nb_columns} columns"
