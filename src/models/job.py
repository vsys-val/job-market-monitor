from dataclasses import dataclass


@dataclass
class Job:
    titulo: str
    empresa: str
    localizacao: str
    url: str
    