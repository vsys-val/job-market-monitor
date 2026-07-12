from api.remotive import buscar_vagas


vagas = buscar_vagas("data")

print(vagas[0])
print(vagas[0].titulo)
