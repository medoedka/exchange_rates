import datetime
import gspread
import json
import requests
import xmltodict
from oauth2client.service_account import ServiceAccountCredentials

# подключение к рабочему листу в google spreadsheets
credentials = ServiceAccountCredentials.from_json_keyfile_name('path_to_credential_file')
googlesheet = gspread.authorize(credentials)
worksheets = googlesheet.open("name_of_worksheet").sheet1

# текущая дата (день/месяц/год)
today = datetime.datetime.now()

# получение данных с российского центробанка и запись данных в переменные
rus_currencies = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(today.strftime('%d/%m/%Y')))
rus_currencies_xml = xmltodict.parse(rus_currencies.text)
rus_currencies_json = json.loads(json.dumps(rus_currencies_xml))
usd_rub = rus_currencies_json['ValCurs']['Valute'][10]['Value']
eur_rub = rus_currencies_json['ValCurs']['Valute'][11]['Value']
pln_rub = rus_currencies_json['ValCurs']['Valute'][19]['Value']
usd_rub, eur_rub, pln_rub = float(usd_rub.replace(',', '.')), float(eur_rub.replace(',', '.')),\
                            float(pln_rub.replace(',', '.'))

# получение данных с белорусского народного банка и запись данных в переменные
usd_byn = requests.get('https://www.nbrb.by/api/exrates/rates/usd?parammode=2').json()['Cur_OfficialRate']
eur_byn = requests.get('https://www.nbrb.by/api/exrates/rates/eur?parammode=2').json()['Cur_OfficialRate']
pln_byn = requests.get('https://www.nbrb.by/api/exrates/rates/pln?parammode=2').json()['Cur_OfficialRate']
rub_byn = requests.get('https://www.nbrb.by/api/exrates/rates/rub?parammode=2').json()['Cur_OfficialRate']
usd_byn, eur_byn, pln_byn, rub_byn = float(usd_byn), float(eur_byn), float(pln_byn), float(rub_byn)

# добавление данных в подключенный лист google spreadsheet
worksheets.append_row([today.strftime('%Y-%m-%d'), usd_byn, eur_byn, rub_byn, pln_byn, usd_rub, eur_rub, pln_rub])
