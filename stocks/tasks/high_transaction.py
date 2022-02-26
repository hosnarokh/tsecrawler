import requests
from bs4 import BeautifulSoup
from stocks.models import HighTransactionReportMinute
print("-----------------------------------------")


def extract_high_transaction_data():
    data = []
    page = requests.get("http://tsetmc.com/Loader.aspx?Partree=151316&Type=MostVisited&Flow=1")
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'table1'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])



def create_high_transaction_report(data):
    for record in data:
        HighTransactionReportMinute.objects.create()




extract_high_transaction_data()
