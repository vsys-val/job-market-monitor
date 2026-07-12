from api.remotive import buscar_vagas


vagas = buscar_vagas("data")

print(f"{len(vagas)} vagas encontradas.")
print(vagas[0].keys())