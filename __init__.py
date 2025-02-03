import azure.functions as func
import re
import json

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\\D', '', cpf)
    if len(cpf) != 11 or cpf in (str(i) * 11 for i in range(10)):
        return False

    def calcular_digito(cpf_parcial):
        soma = sum(int(d) * peso for d, peso in zip(cpf_parcial, range(len(cpf_parcial) + 1, 1, -1)))
        return str((soma * 10) % 11 if (soma * 10) % 11 < 10 else 0)

    return cpf[-2:] == calcular_digito(cpf[:9]) + calcular_digito(cpf[:10])

def main(req: func.HttpRequest) -> func.HttpResponse:
    cpf = req.params.get('cpf')
    if not cpf:
        return func.HttpResponse("Parâmetro 'cpf' é obrigatório.", status_code=400)

    valido = validar_cpf(cpf)
    return func.HttpResponse(json.dumps({"cpf": cpf, "valido": valido}), mimetype="application/json")
