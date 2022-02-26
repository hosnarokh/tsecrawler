import requests
from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from stocks.models import Stock, ImpactOnTheIndexReportMinute, ImpactOnTheIndexReportSecond, \
    ImpactOnTheIndexReportTenSecond

print("-----------------------------------------")
app = Celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 10 seconds.
    sender.add_periodic_task(crontab(second='*/10',
                                     hour='9,10,11,12', day_of_week='sat,sun,mon,tue,wed,thu,fri'),
                             create_impact_on_index_report.s(settings.EVERY_TEN_SECONDS))

    # Calls every seconds
    sender.add_periodic_task(crontab(second='*/1',
                                     hour='9,10,11,12', day_of_week='sat,sun,mon,tue,wed,thu,fri'),
                             create_impact_on_index_report.s(settings.EVERY_SECONDS))

    # Executes every minutes.
    sender.add_periodic_task(
        crontab(minute='*/1',
                hour='9,10,11,12', day_of_week='sat,sun,mon,tue,wed,thu,fri'),
        create_impact_on_index_report.s(settings.EVERY_MINUTES),
    )


def extract_impact_on_index_data():
    data = []
    print("aabba")
    page = requests.get("http://tsetmc.com/Loader.aspx?Partree=151316&Type=MostVisited&Flow=1",
                        timeout=settings.TIME_OUT_REQUEST)
    if page.status_code == '200':
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', attrs={'class': 'table1'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            print("cccc")
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele.encode('ascii', 'ignore') for ele in cols if ele])
    return data


@app.task
def create_impact_on_index_report(data_type):
    # data = extract_impact_on_index_data()[:10]
    data = [['نوري', 'پتروشيمي نوري', '86,900', '486.39'], ['رمپنا', 'گروه مپنا (سهامي عام)', '13,230', '370.3'],
            ['وبملت', 'بانك ملت', '3,539', '305.63'], ['خودرو', 'ايران\u200c خودرو', '2,215', '294.35'],
            ['وغدير', 'سرمايه\u200cگذاري\u200cغدير(هلدينگ\u200c', '12,540', '216.17'],
            ['فخوز', 'فولاد  خوزستان', '4,840', '(180.14)'],
            ['پارسان', 'گسترش نفت و گاز پارسيان', '23,780', '(172.26)'],
            ['فسبزوار', 'پارس فولاد سبزوار', '35,140', '159.13'], ['شتران', 'پالايش نفت تهران', '4,370', '144.62'],
            ['فارس', 'صنايع پتروشيمي خليج فارس', '10,960', '143.62']]
    if data:
        if data_type == settings.EVERY_MINUTES:
            ImpactOnTheIndexReportMinute.objects.filter(active=True).update(active=False)
        elif data_type == settings.EVERY_SECONDS:
            ImpactOnTheIndexReportSecond.objects.filter(active=True).update(active=False)
        elif data_type == settings.EVERY_TEN_SECONDS:
            ImpactOnTheIndexReportTenSecond.objects.filter(active=True).update(active=False)
        for record in data:
            stock, created = Stock.objects.get_or_create(title=record[1].encode('ascii', 'ignore'),
                                                         symbol=record[0].encode('ascii', 'ignore'))
            if data_type == settings.EVERY_MINUTES:
                print("minute")
                ImpactOnTheIndexReportMinute.objects.create(stock=stock, final_value=record[2], impact=record[3])
            elif data_type == settings.EVERY_SECONDS:
                print("sec")
                ImpactOnTheIndexReportSecond.objects.create(stock=stock, final_value=record[2], impact=record[3])
            elif data_type == settings.EVERY_TEN_SECONDS:
                print("10 sec")
                ImpactOnTheIndexReportTenSecond.objects.create(stock=stock, final_value=record[2], impact=record[3])
    else:
        create_impact_on_index_report.retry()
