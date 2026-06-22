from dataclasses import dataclass


@dataclass
class CodeChunk:
    chunk: str
    file: str
    function: str | None = None
    class_name: str | None = None