from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
import json
import pandas as pd


def lambda_handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    chrome = webdriver.Chrome(options=options, service=service)
    PROCURADOS_POLICIA_CIVIL = "https://www.policiacivil.sp.gov.br/portal/faces/pages_home/servicos/procuradosJustica"
    chrome.get(PROCURADOS_POLICIA_CIVIL)
    paragraphs = []
    
    for p in chrome.find_elements(By.TAG_NAME,'p'):
        paragraphs.append(p.text)
   
    print(paragraphs)
    tabela_procuradosJustica = pd.DataFrame({'procuradosJustica':paragraphs})
    tabela_procuradosJustica.dropna(inplace=True)
    print(tabela_procuradosJustica)
    tabela_procuradosJustica = tabela_procuradosJustica.to_dict(orient='records')

    body = {
        "statusCode":200,
        "procuradosJustica":tabela_procuradosJustica
    }
    body = json.dumps(body)
    print(body)

    return body