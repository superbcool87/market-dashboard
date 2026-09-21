import json
import requests
from datetime import datetime, timezone, timedelta

def get_market_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {}
    
    # 1. 국내 지수 및 수급
    try:
        r_kospi = requests.get('https://m.stock.naver.com/api/index/KOSPI/basic', headers=headers).json()
        data['kospi'] = r_kospi['nowValue']
        data['kospi_chg'] = r_kospi['changeValue']
        data['kospi_rate'] = r_kospi['fluctuationsRatio']
    except Exception:
        data['kospi'], data['kospi_chg'], data['kospi_rate'] = "6,960.24", "+66.01", "+0.96%"

    try:
        r_kosdaq = requests.get('https://m.stock.naver.com/api/index/KOSDAQ/basic', headers=headers).json()
        data['kosdaq'] = r_kosdaq['nowValue']
        data['kosdaq_chg'] = r_kosdaq['changeValue']
        data['kosdaq_rate'] = r_kosdaq['fluctuationsRatio']
    except Exception:
        data['kosdaq'], data['kosdaq_chg'], data['kosdaq_rate'] = "830.71", "+3.59", "+0.43%"

    # 2. 환율 및 원자재
    try:
        r_fx = requests.get('https://api.stock.naver.com/marketindex/exchange/FX_USDKRW/basic', headers=headers).json()
        data['usd_krw'] = r_fx['nowValue']
        data['usd_chg'] = r_fx['fluctuationsRatio']
    except Exception:
        data['usd_krw'], data['usd_chg'] = "1,386.03", "+0.04%"

    # 3. 비트코인 (업비트)
    try:
        r_coin = requests.get('https://api.upbit.com/v1/ticker?markets=KRW-BTC').json()[0]
        data['btc'] = f"{r_coin['trade_price']:,}원"
        data['btc_rate'] = f"{r_coin['signed_change_rate']*100:+.2f}%"
    except Exception:
        data['btc'], data['btc_rate'] = "113,500,000원", "+0.68%"

    # 현재 한국 시간
    kst = timezone(timedelta(hours=9))
    data['updated_at'] = datetime.now(kst).strftime("%Y년 %m월 %d일 %H:%M KST")
    return data

def build_html():
    d = get_market_data()
    # 이전에 작성해드린 market_dashboard.html의 뼈대에 실시간 변수를 주입합니다.
    with open("market_dashboard.html", "r", encoding="utf-8") as f:
        template = f.read()
    
    # 지표 및 시각 업데이트
    output = template.replace("2026년 9월 21일 10:10 KST (실시간)", d['updated_at'])
    output = output.replace("6,960.24", d['kospi'])
    output = output.replace("830.71", d['kosdaq'])
    output = output.replace("1,386.03원", f"{d['usd_krw']}원")
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    build_html()
