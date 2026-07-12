from dataclasses import dataclass


@dataclass
class Job:
    titulo: str
    empresa: str
    localizacao: str
    url: str
    categoria: str | None
    tipo_contrato: str | None
    data_publicacao: str | None
    salario: str | None
    fonte: str