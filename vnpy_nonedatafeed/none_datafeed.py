from typing import List, Optional
from pytz import timezone
from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.object import BarData, TickData, HistoryRequest

CHINA_TZ = timezone("Asia/Shanghai")


class NoneDatafeed(BaseDatafeed):

    def __init__(self):
        pass

    def query_bar_history(self, req: HistoryRequest) -> Optional[List[BarData]]:
        return

    def query_tick_history(self, req: HistoryRequest) -> Optional[List[TickData]]:
        return
