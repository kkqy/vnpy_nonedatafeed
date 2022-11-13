from datetime import timedelta
from typing import List, Optional
from pytz import timezone
import traceback

import pandas as pd
from tqsdkpy import tqsdkpy

from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.setting import SETTINGS
from vnpy.trader.constant import Interval
from vnpy.trader.object import BarData, TickData, HistoryRequest


INTERVAL_VT2TQ = {
    Interval.MINUTE: 60,
    Interval.HOUR: 60 * 60,
    Interval.DAILY: 60 * 60 * 24,
    Interval.TICK: 0
}

CHINA_TZ = timezone("Asia/Shanghai")


class TqsdkpyDatafeed(BaseDatafeed):
    """天勤TQsdk数据服务接口"""

    def __init__(self):
        pass

    def query_bar_history(self, req: HistoryRequest) -> Optional[List[BarData]]:
        """查询k线数据"""
        # 初始化API
        try:
            api = tqsdkpy.Client('wss://api.shinnytech.com/t/nfmd/front/mobile')
        except Exception:
            traceback.print_exc()
            return None

        # 查询数据
        tq_symbol = f"{req.exchange.value}.{req.symbol}"

        data = api.get_kline_data_series(
            symbol=tq_symbol,
            duration_seconds=INTERVAL_VT2TQ[req.interval],
            start_dt=req.start,
            end_dt=(req.end + timedelta(1))
        )

        # 关闭API
        api.close()

        # 解析数据
        bars: List[BarData] = []

        if data is not None:
            for tp in data:
                # 天勤时间为与1970年北京时间相差的秒数，需要加上8小时差
                dt = pd.Timestamp(tp['datetime']).to_pydatetime() + timedelta(hours=8)

                bar = BarData(
                    symbol=req.symbol,
                    exchange=req.exchange,
                    interval=req.interval,
                    datetime=CHINA_TZ.localize(dt),
                    open_price=tp['open'],
                    high_price=tp['high'],
                    low_price=tp['low'],
                    close_price=tp['close'],
                    volume=tp['volume'],
                    open_interest=tp['open_oi'],
                    gateway_name="TQ",
                )
                bars.append(bar)

        return bars

    def query_tick_history(self, req: HistoryRequest) -> Optional[List[TickData]]:
        """查询Tick数据"""
        # 初始化API
        try:
            api = tqsdkpy.Client('wss://api.shinnytech.com/t/nfmd/front/mobile')
        except Exception:
            traceback.print_exc()
            return None

        # 查询数据
        tq_symbol = f"{req.exchange.value}.{req.symbol}"

        datas = api.get_tick_data_series(
            symbol=tq_symbol,
            start_dt=req.start,
            end_dt=(req.end + timedelta(1))
        )

        # 关闭API
        api.close()

        # 解析数据
        ticks: List[TickData] = []

        if datas is not None:
            for tp in datas:
                # 天勤时间为与1970年北京时间相差的秒数，需要加上8小时差
                if tp['last_price'] is not None:
                    dt = pd.Timestamp(tp['datetime']).to_pydatetime() + timedelta(hours=8)

                    tick = TickData(
                        symbol=req.symbol,
                        exchange=req.exchange,
                        datetime=CHINA_TZ.localize(dt),
                        high_price=tp['highest'],
                        low_price=tp['lowest'],
                        last_price=tp['last_price'],
                        volume=tp['volume'],
                        turnover=tp['amount'],
                        open_interest=tp['open_interest'],
                        bid_price_1=tp['bid_price1'],
                        ask_price_1=tp['ask_price1'],
                        bid_volume_1=tp['bid_volume1'],
                        ask_volume_1=tp['ask_volume1'],
                        bid_price_2=tp['bid_price2'],
                        ask_price_2=tp['ask_price2'],
                        bid_volume_2=tp['bid_volume2'],
                        ask_volume_2=tp['ask_volume2'],
                        bid_price_3=tp['bid_price3'],
                        ask_price_3=tp['ask_price3'],
                        bid_volume_3=tp['bid_volume3'],
                        ask_volume_3=tp['ask_volume3'],
                        bid_price_4=tp['bid_price4'],
                        ask_price_4=tp['ask_price4'],
                        bid_volume_4=tp['bid_volume4'],
                        ask_volume_4=tp['ask_volume4'],
                        bid_price_5=tp['bid_price5'],
                        ask_price_5=tp['ask_price5'],
                        bid_volume_5=tp['bid_volume5'],
                        ask_volume_5=tp['ask_volume5'],
                        gateway_name="TQ",
                    )
                    ticks.append(tick)

        return ticks
