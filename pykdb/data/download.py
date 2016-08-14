# -*- coding: utf-8 -*-
import time
import urllib.error
import urllib.request

import pandas as pd

_SLEEP_TIME = 2.5


def download_csv(url) -> pd.DataFrame:
    """
    urlで指定したデータをDataFrameで取得する. 取得可能でなければ空のDataFrameを返す
    :param url:
    :return:
    """
    try:
        df = pd.read_csv(urllib.request.urlopen(url), encoding='Shift_JIS')
    except ValueError:
        df = pd.DataFrame()
    finally:
        time.sleep(_SLEEP_TIME)
    return df
