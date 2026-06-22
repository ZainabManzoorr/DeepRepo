from dataclasses import dataclass


@dataclass
class Document:
    file: str
    path: str
    type: str
    content: str