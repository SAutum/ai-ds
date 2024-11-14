from typing import Any

Column = list[Any]
Relation = dict[str, Column]


def join(relation1: Relation, relation2: Relation) -> Relation:
    # Your solution goes here.
