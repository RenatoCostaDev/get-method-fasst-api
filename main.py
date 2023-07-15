from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import urllib.request, json

app = FastAPI()
templates = Jinja2Templates(directory='templates')

def get_data_url(url):
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    json_data = json.loads(dados)
    dados_covid = json_data['data']

    return dados_covid

def organize_case_list(case_list):
    sorted_case_list = sorted(case_list, key=lambda x: x['suspects'], reverse=True)
    return sorted_case_list

def organize_case_list_reverse(case_list):
    sorted_case_list = sorted(case_list, key=lambda x: x['suspects'], reverse=False)
    return sorted_case_list

@app.get("/covid", response_class=HTMLResponse)
def read_root(request: Request): 
    url = 'https://covid19-brazil-api.vercel.app/api/report/v1'
    dados_covid = get_data_url(url)

    return templates.TemplateResponse(
        'covid.html',
        {"request": request, 'dados_covid': dados_covid }
    )

@app.get("/covid/desc", response_class=HTMLResponse)
def read_desc(request: Request):
    url = 'https://covid19-brazil-api.vercel.app/api/report/v1'
    dados_covid = get_data_url(url)
    organized_desc = organize_case_list(dados_covid)

    return templates.TemplateResponse(
        'desc.html',
        {"request": request, 'organized_desc': organized_desc }
    )

@app.get("/covid/cresc", response_class=HTMLResponse)
def read_cresc(request: Request):
    url = 'https://covid19-brazil-api.vercel.app/api/report/v1'
    dados_covid = get_data_url(url)
    organized_cresc = organize_case_list_reverse(dados_covid)

    return templates.TemplateResponse(
        'cresc.html',
        {"request": request, 'organized_cresc': organized_cresc }
    )