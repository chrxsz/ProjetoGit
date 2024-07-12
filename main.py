from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

mes_arquivos = {
    'janeiro': '',
    'fevereiro': '',
    'março': '',
    'abril': '',
    'maio': '',
    'junho': '/content/drive/MyDrive/boletosjunho23.csv',
    'julho': '',
    'agosto': '',
    'setembro': '',
    'outubro': '',
    'novembro': '',
    'dezembro': ''
}

@app.get("/verificar/")
async def verificar_cpf_cnpj(mes: str, cpf_cnpj: str):
    mes = mes.lower()

    if mes not in mes_arquivos:
        raise HTTPException(status_code=400, detail="Mês inválido ou escreva o mês com todas as letras minúsculas")

    arquivo = mes_arquivos[mes]

    if not arquivo:
        raise HTTPException(status_code=404, detail=f"Arquivo para o mês {mes} não encontrado.")

    try:
        df = pd.read_csv(arquivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Erro ao carregar o arquivo CSV.")

    df['ID'] = df['ID'].str.replace('.pdf', '', regex=False)

    if cpf_cnpj in df['ID'].values:
        link = df[df['ID'] == cpf_cnpj]['Link'].values[0]
        return {"mensagem": f"O link correspondente ao CPF/CNPJ {cpf_cnpj} é {link}"}
    else:
        raise HTTPException(status_code=404, detail=f"O CPF/CNPJ {cpf_cnpj} é inválido.")