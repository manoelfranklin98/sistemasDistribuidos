from dataclasses import dataclass, asdict

@dataclass
class Contato:
    id: int
    nome: str
    telefone: str
    email: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Contato(d['id'], d['nome'], d['telefone'], d['email'])
