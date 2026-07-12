from api.remotive import buscar_vagas
from database.sqlite import criar_tabela, salvar_vagas


criar_tabela()

vagas = buscar_vagas("data")

salvar_vagas(vagas)

print(f"{len(vagas)} vagas processadas.")