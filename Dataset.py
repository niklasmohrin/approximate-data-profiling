from dataclasses import dataclass


@dataclass
class Dataset:
    name: str
    filename: str
    separator: str = ";"
