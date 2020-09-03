import requests
import pandas as pd
import datetime
import json

milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000

r = requests.post('https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t='+str(milliseconds_since_epoch), data = {'key':'value'})

data = json.loads(r.text)
data = pd.json_normalize(data["rows"])

data.columns = [column[5:] for column in data.columns]

column_name = {
    "bond_id": "可转债代码",
    "bond_nm": "转债名称",
    "price": "可转债现价",
    "increase_rt": "可转债涨跌幅",
    "stock_id": "正股代码",
    "stock_nm": "正股名称",
    "sprice": "正股价格",
    "sincrease_rt": "正股涨跌幅",
    "convert_value": "转股价值",
    "premium_rt": "溢价率",
    "convert_price": "转股价",
    "convert_dt": "转股起始日",
    "maturity_dt": "到期日",
    "force_redeem_price": "强赎触发价",
    "force_redeem": "强制赎回情况",
    "redeem_flag": "是否强制赎回",
    "rating_cd": "债券评级",
    "issuer_rating_cd": "主体评级",
    "guarantor": "担保",
    "convert_cd": "转股代码",
    "ytm_rt": "到期税前收益",
    "ytm_rt_tax": "到期税后收益",
    "price_tips": "价格说明",

    "convert_price_valid_from": "转股价生效日",
    "next_put_dt": "回售起始日",
    "redeem_price": "赎回价",
    "redeem_dt": "强制赎回日期",
    "real_force_redeem_price": "强制赎回价格",
    "orig_iss_amt": "发行规模（亿）",
    "curr_iss_amt": "剩余规模（亿）",
    "repo_cd": "质押代码",
    "ration_rt": "股东配售率",
    "pb": "市净率",
    "total_shares": "总股数",
    "year_left": "剩余年限",
    "put_convert_price": "回售触发价",
    "convert_cd_tip": "转股说明"
}

data = data[column_name.keys()]


def redeem_flag(x):
    if x == "N":
        return "放弃强制赎回"
    elif x == "X":
        return "未触发强赎条件"
    elif x == "Y":
        return "强制赎回"


data["redeem_flag"] = data["redeem_flag"].apply(redeem_flag)

def ration_rt(x):
    if x:
        return '{:.2%}'.format(float(x)/100)


data["ration_rt"] = data["ration_rt"].apply(ration_rt)

data["stock_id"] = data["stock_id"].apply(lambda x: x[2:])

data["premium_rt"] = data["premium_rt"].apply(lambda x: float(x[:-1])/100)

data = data.rename(columns=column_name)

# data.to_csv("cb.csv",index=False,encoding="utf_8_sig")
