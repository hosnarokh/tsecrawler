from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.custom_fields import FarsiCharField
from utils.custom_models import BaseModel, TimeStampModel


class Stock(BaseModel):
    title = FarsiCharField(_('title'), max_length=50)
    symbol = FarsiCharField(_('symbol'), max_length=50, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')


class HighTransactionStock(TimeStampModel):
    yesterday_price = models.CharField(_('yesterday price'), max_length=10)
    final_price = models.CharField(_('final price'), max_length=10)
    final_transaction_price = models.CharField(_('final transaction price'), max_length=10)
    min_price = models.CharField(_('min price'), max_length=10)
    max_price = models.CharField(_('max price'), max_length=10)
    quantity = models.PositiveIntegerField(_('quantity'))
    volume = models.CharField(_('volume'), max_length=100)
    value = models.CharField(_('value'), max_length=100)

    def __str__(self):
        return f'{self.yesterday_price}-{self.stock.title}'

    class Meta:
        abstract = True
        verbose_name = _('High Transaction Stock')
        verbose_name_plural = _('High Transaction Stocks')


class HighTransactionReportMinute(HighTransactionStock):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='high_transactions_minute',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_minute', editable=False)

    class Meta:
        verbose_name = _('High Transaction Report Minute')
        verbose_name_plural = _('High Transaction Reports Minute')


class HighTransactionReportTenSecond(HighTransactionStock):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='high_transactions_ten_second',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='ten_second', editable=False)

    class Meta:
        verbose_name = _('High Transaction Report Ten Second')
        verbose_name_plural = _('High Transaction Reports Ten Second')


class HighTransactionReportSecond(HighTransactionStock):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='high_transactions_second',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_second', editable=False)

    class Meta:
        verbose_name = _('High Transaction Report Second')
        verbose_name_plural = _('High Transaction Reports Second')


class Index(BaseModel):
    title = FarsiCharField(_('title'), max_length=50)
    symbol = FarsiCharField(_('symbol'), max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Index')
        verbose_name_plural = _('Indexs')


class IndexReport(TimeStampModel):
    published_time = models.TimeField(_('published time'), auto_now_add=True, db_index=True)
    final_value = models.CharField(_('final value'), max_length=10)
    change_value = models.CharField(_('change value'), max_length=10)
    percent = models.CharField(_('percent'), max_length=10)
    max_value = models.CharField(_('max value'), max_length=10)
    min_value = models.CharField(_('min value'), max_length=10)

    def __str__(self):
        return f'{self.index.title}-{self.published_time}'

    class Meta:
        abstract = True
        verbose_name = _('Index Report')
        verbose_name_plural = _('Index Reports')


class IndexReportMinute(IndexReport):
    index = models.ForeignKey(Index, verbose_name=_('index'), related_name='index_report_minutes',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_minute', editable=False)

    class Meta:
        verbose_name = _('Index Report Minute')
        verbose_name_plural = _('Index Reports Minute')


class IndexReportTenSecond(IndexReport):
    index = models.ForeignKey(Index, verbose_name=_('index'), related_name='index_report_ten_seconds',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_second', editable=False)

    class Meta:
        verbose_name = _('IndexReport Ten Second')
        verbose_name_plural = _('Index Reports Ten Second')


class IndexReportSecond(IndexReport):
    index = models.ForeignKey(Index, verbose_name=_('index'), related_name='index_report_seconds',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_second', editable=False)

    class Meta:
        verbose_name = _('Index Report Second')
        verbose_name_plural = _('Index Reports Second')


class ImpactOnTheIndexReport(TimeStampModel):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='impact_report',
                              on_delete=models.CASCADE)

    final_value = models.CharField(_('final value'), max_length=10)
    impact = models.CharField(_('impact'), max_length=10)

    class Meta:
        abstract = True
        verbose_name = _('Impact On The Index Report')
        verbose_name_plural = _('Impact On The Index Reports')


class ImpactOnTheIndexReportMinute(ImpactOnTheIndexReport):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='impact_report_minutes',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_minute', editable=False)

    class Meta:
        verbose_name = _('Impact On The Index Report Minute')
        verbose_name_plural = _('Impact On The Index Reports Minute')


class ImpactOnTheIndexReportTenSecond(ImpactOnTheIndexReport):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='impact_report_ten_seconds',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_second', editable=False)

    class Meta:
        verbose_name = _('Impact On The Index Report Ten Second')
        verbose_name_plural = _('Impact On The Index Reports Ten Second')


class ImpactOnTheIndexReportSecond(ImpactOnTheIndexReport):
    stock = models.ForeignKey(Stock, verbose_name=_('stock'), related_name='impact_report_seconds',
                              on_delete=models.CASCADE)
    report_type = models.CharField('report type', max_length=10, default='per_second', editable=False)

    class Meta:
        verbose_name = _('Impact On The Index Report Second')
        verbose_name_plural = _('Impact On The Index Reports Second')
