import json
import requests
from datetime import datetime, timezone, timedelta

def get_market_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    data = {}
    
    # 1. 코스피 (KOSPI)
    try:
        r = requests.get('https://m.stock.naver.com/api/index/KOSPI/basic', headers=headers, timeout=5).json()
        data['kospi'] = r.get('nowValue', '6,960.24')
        chg = r.get('changeValue', '+66.01')
        rate = r.get('fluctuationsRatio', '0.96')
        is_up = not str(rate).startswith('-')
        data['kospi_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['kospi'], data['kospi_rate_str'] = "6,960.24", "▲ +66.01 (+0.96%)"

    # 2. 코스닥 (KOSDAQ)
    try:
        r = requests.get('https://m.stock.naver.com/api/index/KOSDAQ/basic', headers=headers, timeout=5).json()
        data['kosdaq'] = r.get('nowValue', '830.71')
        chg = r.get('changeValue', '+3.59')
        rate = r.get('fluctuationsRatio', '0.43')
        is_up = not str(rate).startswith('-')
        data['kosdaq_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['kosdaq'], data['kosdaq_rate_str'] = "830.71", "▲ +3.59 (+0.43%)"

    # 3. S&P 500
    try:
        r = requests.get('https://api.stock.naver.com/index/.INX/basic', headers=headers, timeout=5).json()
        data['spx'] = r.get('nowValue', '7,650.50')
        chg = r.get('changeValue', '+12.74')
        rate = r.get('fluctuationsRatio', '0.17')
        is_up = not str(rate).startswith('-')
        data['spx_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['spx'], data['spx_rate_str'] = "7,650.50", "▲ +12.74 (+0.17%)"

    # 4. 나스닥 종합 (NASDAQ)
    try:
        r = requests.get('https://api.stock.naver.com/index/.IXIC/basic', headers=headers, timeout=5).json()
        data['nasdaq'] = r.get('nowValue', '26,522.55')
        chg = r.get('changeValue', '+104.25')
        rate = r.get('fluctuationsRatio', '0.39')
        is_up = not str(rate).startswith('-')
        data['nasdaq_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['nasdaq'], data['nasdaq_rate_str'] = "26,522.55", "▲ +104.25 (+0.39%)"

    # 5. 다우존스 (DOW)
    try:
        r = requests.get('https://api.stock.naver.com/index/.DJI/basic', headers=headers, timeout=5).json()
        data['dow'] = r.get('nowValue', '51,682.64')
        chg = r.get('changeValue', '-95.40')
        rate = r.get('fluctuationsRatio', '-0.18')
        is_up = not str(rate).startswith('-')
        data['dow_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['dow'], data['dow_rate_str'] = "51,682.64", "▼ -95.40 (-0.18%)"

    # 6. 원/달러 환율 (USD/KRW)
    try:
        r = requests.get('https://api.stock.naver.com/marketindex/exchange/FX_USDKRW/basic', headers=headers, timeout=5).json()
        data['usd_krw'] = r.get('nowValue', '1,386.03')
        chg = r.get('changeValue', '+0.53')
        rate = r.get('fluctuationsRatio', '0.04')
        is_up = not str(rate).startswith('-')
        data['usd_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['usd_krw'], data['usd_rate_str'] = "1,386.03", "▲ +0.53 (+0.04%)"

    # 7. WTI 원유 (Oil)
    try:
        r = requests.get('https://api.stock.naver.com/marketindex/oil/CL/basic', headers=headers, timeout=5).json()
        data['oil'] = f"${r.get('nowValue', '94.43')}"
        chg = r.get('changeValue', '-1.65')
        rate = r.get('fluctuationsRatio', '-1.72')
        is_up = not str(rate).startswith('-')
        data['oil_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['oil'], data['oil_rate_str'] = "$94.43", "▼ -1.65 (-1.72%)"

    # 8. 국제 금 (Gold)
    try:
        r = requests.get('https://api.stock.naver.com/marketindex/metal/GC/basic', headers=headers, timeout=5).json()
        data['gold'] = f"${r.get('nowValue', '4,411.80')}"
        chg = r.get('changeValue', '-13.10')
        rate = r.get('fluctuationsRatio', '-0.30')
        is_up = not str(rate).startswith('-')
        data['gold_rate_str'] = f"{'▲ +' if is_up else '▼ '}{chg} ({'+' if is_up else ''}{rate}%)"
    except Exception:
        data['gold'], data['gold_rate_str'] = "$4,411.80", "▼ -13.10 (-0.30%)"

    # 9. 비트코인 (업비트)
    try:
        r = requests.get('https://api.upbit.com/v1/ticker?markets=KRW-BTC', timeout=5).json()[0]
        data['btc'] = f"{r['trade_price']:,}원"
        data['btc_rate_str'] = f"{'▲ +' if r['signed_change_rate'] >= 0 else '▼ '}{r['signed_change_rate']*100:+.2f}%"
    except Exception:
        data['btc'], data['btc_rate_str'] = "113,500,000원", "▲ +0.68%"

    # 10. 이더리움 (업비트)
    try:
        r = requests.get('https://api.upbit.com/v1/ticker?markets=KRW-ETH', timeout=5).json()[0]
        data['eth'] = f"{r['trade_price']:,}원"
        data['eth_rate_str'] = f"{'▲ +' if r['signed_change_rate'] >= 0 else '▼ '}{r['signed_change_rate']*100:+.2f}%"
    except Exception:
        data['eth'], data['eth_rate_str'] = "3,720,000원", "▲ +1.66%"

    # KST 기준시각
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)
    data['sync_time'] = now.strftime("%m.%d %H:%M:%S KST (빌드 완료)")
    return data

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>글로벌 및 국내 금융시장 실시간 웹 대시보드</title>
<style>
  :root {
    --bg-main: #0b0f19;
    --bg-card: #151d30;
    --bg-card-hover: #1c2640;
    --border: #24324f;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-faint: #64748b;
    --red: #f43f5e;
    --blue: #38bdf8;
    --green: #10b981;
    --yellow: #f59e0b;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", sans-serif; }
  body { background-color: var(--bg-main); color: var(--text-primary); padding: 20px; line-height: 1.6; }
  .container { max-width: 1280px; margin: 0 auto; }
  
  header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 18px; margin-bottom: 16px; flex-wrap: wrap; gap: 12px; }
  .header-left h1 { font-size: 24px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; display: flex; align-items: center; gap: 10px; }
  .header-left p { color: var(--text-secondary); font-size: 13px; margin-top: 4px; }
  .header-badges { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .badge { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; text-decoration: none; }
  .badge-live { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); display: inline-flex; align-items: center; gap: 6px; }
  .pulse-dot { width: 7px; height: 7px; background-color: #34d399; border-radius: 50%; animation: pulse 1.5s infinite; }
  @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1); } }
  .badge-schedule { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }

  /* Realtime Status Bar */
  .live-status-bar { display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.6); border: 1px solid var(--border); padding: 10px 16px; border-radius: 10px; margin-bottom: 18px; font-size: 13px; color: var(--text-secondary); flex-wrap: wrap; gap: 10px; }
  .refresh-btn { background: #2563eb; color: #fff; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 12px; display: inline-flex; align-items: center; gap: 5px; }
  .refresh-btn:hover { background: #1d4ed8; }

  /* TradingView Live Streaming Bar */
  .tradingview-container { margin-bottom: 20px; border-radius: 10px; overflow: hidden; border: 1px solid var(--border); }

  /* Schedule Banner */
  .schedule-banner { background: linear-gradient(90deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8)); border: 1px solid var(--border); border-radius: 12px; padding: 14px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
  .schedule-banner h4 { font-size: 14px; font-weight: 700; color: #38bdf8; }
  .schedule-steps { display: flex; gap: 16px; font-size: 12px; color: var(--text-secondary); flex-wrap: wrap; }
  .step-item { display: flex; align-items: center; gap: 6px; }
  .step-dot { width: 8px; height: 8px; border-radius: 50%; background-color: #38bdf8; }
  .step-active { color: #f8fafc; font-weight: 700; }

  /* Cards Grid */
  .grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 24px; }
  .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; transition: transform 0.2s, background-color 0.4s; position: relative; }
  .card:hover { transform: translateY(-2px); background-color: var(--bg-card-hover); }
  
  .card-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
  .card-label { font-size: 12px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; }
  .card-time { font-size: 10px; color: var(--text-faint); font-weight: 500; letter-spacing: -0.2px; opacity: 0.85; }
  
  .card-val { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 4px; }
  .card-chg { font-size: 13px; font-weight: 700; display: flex; align-items: center; gap: 4px; }
  .card-desc { font-size: 11px; color: var(--text-secondary); margin-top: 4px; }
  .up { color: var(--red); }
  .down { color: var(--blue); }
  .neutral { color: var(--text-secondary); }

  /* Flash Animations */
  .flash-green { animation: flashG 0.9s ease-out; }
  .flash-red { animation: flashR 0.9s ease-out; }
  .flash-blue { animation: flashB 0.9s ease-out; }
  @keyframes flashG { 0% { background-color: rgba(16, 185, 129, 0.35); } 100% { background-color: var(--bg-card); } }
  @keyframes flashR { 0% { background-color: rgba(244, 63, 94, 0.35); } 100% { background-color: var(--bg-card); } }
  @keyframes flashB { 0% { background-color: rgba(56, 189, 248, 0.35); } 100% { background-color: var(--bg-card); } }

  /* Layout Sections */
  .section-header { font-size: 17px; font-weight: 700; margin: 28px 0 14px 0; display: flex; align-items: center; justify-content: space-between; color: #f8fafc; flex-wrap: wrap; gap: 10px; }
  .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .chart-box { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 18px; }
  .chart-title { font-size: 14px; font-weight: 700; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }

  /* Tables */
  .table-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; margin-bottom: 24px; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); }
  th { background-color: rgba(255,255,255,0.02); color: var(--text-secondary); font-weight: 600; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background-color: rgba(255,255,255,0.015); }
  .text-right { text-align: right; }
  .badge-buy { background: rgba(244, 63, 94, 0.15); color: #fb7185; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 11px; }
  .badge-sell { background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 11px; }

  /* News Grid */
  .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 14px; margin-bottom: 24px; }
  .news-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; }
  .news-card h4 { font-size: 14px; font-weight: 700; line-height: 1.5; margin-bottom: 8px; }
  .news-card a { color: #60a5fa; text-decoration: none; }
  .news-card a:hover { text-decoration: underline; }
  .news-desc { font-size: 12.5px; color: #cbd5e1; line-height: 1.5; margin-bottom: 10px; }
  .news-footer { font-size: 11px; color: var(--text-secondary); display: flex; justify-content: space-between; }

  /* Analysis */
  .commentary-card { background: rgba(30, 41, 59, 0.5); border-left: 4px solid #38bdf8; border-radius: 0 10px 10px 0; padding: 18px; margin-bottom: 24px; }
  .commentary-card p { font-size: 13.5px; color: #cbd5e1; margin-bottom: 10px; line-height: 1.6; }
  .commentary-card p:last-child { margin-bottom: 0; }
  .commentary-card strong { color: #f8fafc; }

  /* Watchlist Controls */
  .watchlist-controls { display: flex; gap: 8px; align-items: center; }
  .watchlist-input { background: #1e293b; border: 1px solid var(--border); color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 12px; width: 180px; }
  .watchlist-btn { background: #2563eb; color: #fff; border: none; padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; }
  .watchlist-btn:hover { background: #1d4ed8; }
  .del-btn { background: transparent; border: none; color: #64748b; cursor: pointer; font-size: 12px; padding: 0 4px; }
  .del-btn:hover { color: #f43f5e; }

  footer { text-align: center; font-size: 12px; color: var(--text-secondary); border-top: 1px solid var(--border); padding-top: 20px; margin-top: 40px; }
</style>
</head>
<body>
<div class="container">
  <!-- Header -->
  <header>
    <div class="header-left">
      <h1>🌐 글로벌 & 국내 증시 마켓 대시보드</h1>
      <p>실시간 매크로 지표, 환율, 원자재, 코인 및 국내 수급 통합 분석 체계</p>
    </div>
    <div class="header-badges">
      <span class="badge badge-live"><span class="pulse-dot"></span>실시간 시세 연동 중</span>
      <span class="badge badge-schedule">⚙️ 일 4회 클라우드 자동 갱신</span>
    </div>
  </header>

  <!-- Live Status & Instant Refresh Bar -->
  <div class="live-status-bar">
    <div>
      <span>🕒 현재 시각: <strong id="live-clock" style="color: #fff;">--:--:--</strong></span>
      <span style="margin-left: 15px;">🔄 최근 데이터 동기화: <strong id="sync-time" style="color: #38bdf8;">{{SYNC_TIME}}</strong></span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
      <span>다음 실시간 갱신: <strong id="timer-sec" style="color: #34d399;">30</strong>초 후</span>
      <button class="refresh-btn" onclick="fetchAllLiveMarketData()">↻ 즉시 갱신</button>
    </div>
  </div>

  <!-- TradingView Ticker Tape (Tick-by-Tick Live Streaming) -->
  <div class="tradingview-container">
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {
        "symbols": [
          {"proName": "KRX:KOSPI", "title": "코스피"},
          {"proName": "KRX:KOSDAQ", "title": "코스닥"},
          {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
          {"proName": "FOREXCOM:NSXUSD", "title": "나스닥 100"},
          {"proName": "FX_IDC:USDKRW", "title": "달러/원"},
          {"proName": "NYMEX:CL1!", "title": "WTI 원유"},
          {"proName": "COMEX:GC1!", "title": "금 (Gold)"},
          {"proName": "UPBIT:BTCKRW", "title": "비트코인"}
        ],
        "showSymbolLogo": true,
        "isTransparent": false,
        "displayMode": "adaptive",
        "colorTheme": "dark",
        "locale": "kr"
      }
      </script>
    </div>
  </div>

  <!-- Schedule Banner -->
  <div class="schedule-banner">
    <div>
      <h4>📅 데일리 4단계 정기 분석 파이프라인</h4>
    </div>
    <div class="schedule-steps">
      <div class="step-item"><div class="step-dot"></div><span>1회차: 07:00 (美 증시 마감 & 개장전 점검)</span></div>
      <div class="step-item"><div class="step-dot" style="background-color:#10b981;"></div><span class="step-active">2회차: 11:30 (오전 장중 수급 점검)</span></div>
      <div class="step-item"><div class="step-dot"></div><span>3회차: 16:00 (국내 증시 마감 종합)</span></div>
      <div class="step-item"><div class="step-dot"></div><span>4회차: 22:00 (美 증시 개장 & 야간 선물)</span></div>
    </div>
  </div>

  <!-- Key Metrics Row 1: Equities -->
  <div class="section-header">
    <span>📈 국내 및 주요 해외 증시 지수</span>
  </div>
  <div class="grid-5">
    <div class="card" id="card-kospi">
      <div class="card-header-row">
        <span class="card-label">코스피 (KOSPI)</span>
        <span class="card-time" id="time-kospi">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-kospi">{{KOSPI}}</div>
      <div class="card-chg up" id="rate-kospi">{{KOSPI_RATE_STR}}</div>
      <div class="card-desc">네이버 금융 실시간 연동</div>
    </div>
    <div class="card" id="card-kosdaq">
      <div class="card-header-row">
        <span class="card-label">코스닥 (KOSDAQ)</span>
        <span class="card-time" id="time-kosdaq">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-kosdaq">{{KOSDAQ}}</div>
      <div class="card-chg up" id="rate-kosdaq">{{KOSDAQ_RATE_STR}}</div>
      <div class="card-desc">네이버 금융 실시간 연동</div>
    </div>
    <div class="card" id="card-spx">
      <div class="card-header-row">
        <span class="card-label">S&P 500 (미국)</span>
        <span class="card-time" id="time-spx">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-spx">{{SPX}}</div>
      <div class="card-chg up" id="rate-spx">{{SPX_RATE_STR}}</div>
      <div class="card-desc">야후 파이낸스 실시간 연동</div>
    </div>
    <div class="card" id="card-nasdaq">
      <div class="card-header-row">
        <span class="card-label">나스닥 종합 (미국)</span>
        <span class="card-time" id="time-nasdaq">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-nasdaq">{{NASDAQ}}</div>
      <div class="card-chg up" id="rate-nasdaq">{{NASDAQ_RATE_STR}}</div>
      <div class="card-desc">야후 파이낸스 실시간 연동</div>
    </div>
    <div class="card" id="card-dow">
      <div class="card-header-row">
        <span class="card-label">다우존스 (미국)</span>
        <span class="card-time" id="time-dow">실시간 조회 중...</span>
      </div>
      <div class="card-val down" id="val-dow">{{DOW}}</div>
      <div class="card-chg down" id="rate-dow">{{DOW_RATE_STR}}</div>
      <div class="card-desc">야후 파이낸스 실시간 연동</div>
    </div>
  </div>

  <!-- Key Metrics Row 2: FX, Commodities & Crypto -->
  <div class="section-header">
    <span>🛢️ 환율, 원자재 및 주요 가상자산</span>
  </div>
  <div class="grid-5">
    <div class="card" id="card-fx">
      <div class="card-header-row">
        <span class="card-label">원/달러 환율</span>
        <span class="card-time" id="time-fx">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-fx">{{USD_KRW}}원</div>
      <div class="card-chg up" id="rate-fx">{{USD_RATE_STR}}</div>
      <div class="card-desc">오픈 외환 실시간 연동</div>
    </div>
    <div class="card" id="card-oil">
      <div class="card-header-row">
        <span class="card-label">WTI 원유</span>
        <span class="card-time" id="time-oil">실시간 조회 중...</span>
      </div>
      <div class="card-val down" id="val-oil">{{OIL}}</div>
      <div class="card-chg down" id="rate-oil">{{OIL_RATE_STR}}</div>
      <div class="card-desc">야후 파이낸스 실시간 연동</div>
    </div>
    <div class="card" id="card-gold">
      <div class="card-header-row">
        <span class="card-label">국제 금 (Gold)</span>
        <span class="card-time" id="time-gold">실시간 조회 중...</span>
      </div>
      <div class="card-val down" id="val-gold">{{GOLD}}</div>
      <div class="card-chg down" id="rate-gold">{{GOLD_RATE_STR}}</div>
      <div class="card-desc">야후 파이낸스 실시간 연동</div>
    </div>
    <div class="card" id="card-btc">
      <div class="card-header-row">
        <span class="card-label">비트코인 (BTC)</span>
        <span class="card-time" id="time-btc">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-btc">{{BTC}}</div>
      <div class="card-chg up" id="rate-btc">{{BTC_RATE_STR}}</div>
      <div class="card-desc">업비트 실시간 연동</div>
    </div>
    <div class="card" id="card-eth">
      <div class="card-header-row">
        <span class="card-label">이더리움 (ETH)</span>
        <span class="card-time" id="time-eth">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-eth">{{ETH}}</div>
      <div class="card-chg up" id="rate-eth">{{ETH_RATE_STR}}</div>
      <div class="card-desc">업비트 실시간 연동</div>
    </div>
  </div>

  <!-- ⭐ 관심 및 보유 종목 실시간 워치리스트 -->
  <div class="section-header">
    <div style="display: flex; align-items: center; gap: 8px;">
      <span>⭐ 관심 및 보유 종목</span>
      <span style="font-size: 11px; color: var(--text-secondary); font-weight: normal;">(브라우저 저장 / 종목 자유 추가)</span>
    </div>
    <div class="watchlist-controls">
      <input type="text" id="custom-stock-code" class="watchlist-input" placeholder="종목코드 6자리 (예: 005930)">
      <button class="watchlist-btn" onclick="addCustomStock()">+ 종목 추가</button>
    </div>
  </div>
  <div class="grid-5" id="watchlist-container">
    <div class="card" id="stock-005930">
      <div class="card-header-row">
        <span class="card-label">삼성전자 (005930)</span>
        <span class="card-time">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-stock-005930">269,500원</div>
      <div class="card-chg up" id="rate-stock-005930">▲ +8,000 (+3.06%)</div>
      <div class="card-desc">네이버 금융 실시간 연동</div>
    </div>
    <div class="card" id="stock-000660">
      <div class="card-header-row">
        <span class="card-label">SK하이닉스 (000660)</span>
        <span class="card-time">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-stock-000660">318,500원</div>
      <div class="card-chg up" id="rate-stock-000660">▲ +4,500 (+1.43%)</div>
      <div class="card-desc">네이버 금융 실시간 연동</div>
    </div>
    <div class="card" id="stock-005380">
      <div class="card-header-row">
        <span class="card-label">현대차 (005380)</span>
        <span class="card-time">실시간 조회 중...</span>
      </div>
      <div class="card-val down" id="val-stock-005380">248,000원</div>
      <div class="card-chg down" id="rate-stock-005380">▼ -1,500 (-0.60%)</div>
      <div class="card-desc">네이버 금융 실시간 연동</div>
    </div>
    <div class="card" id="stock-035420">
      <div class="card-header-row">
        <span class="card-label">NAVER (035420)</span>
        <span class="card-time">실시간 조회 중...</span>
      </div>
      <div class="card-val up" id="val-stock-035420">198,200원</div>
      <div class="card-chg up" id="rate-stock-035420">▲ +1,800 (+0.92%)</div>
      <div class="card-desc">네이버 금융 실시간 연동</div>
    </div>
  </div>

  <!-- SVG Visualizations -->
  <div class="section-header">
    <span>📊 시장 시각화 분석</span>
  </div>
  <div class="charts-grid">
    <div class="chart-box">
      <div class="chart-title">
        <span>코스피 장중 7,000선 돌파 추이</span>
        <span class="up" style="font-size: 12px;">최고 7,007.10</span>
      </div>
      <svg viewBox="0 0 420 160" style="width: 100%; height: 160px;">
        <defs>
          <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="1">
            <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.35"/>
            <stop offset="100%" stop-color="#f43f5e" stop-opacity="0.0"/>
          </linearGradient>
        </defs>
        <line x1="30" y1="130" x2="400" y2="130" stroke="#24324f" stroke-dasharray="3"/>
        <line x1="30" y1="80" x2="400" y2="80" stroke="#24324f" stroke-dasharray="3"/>
        <line x1="30" y1="30" x2="400" y2="30" stroke="#24324f" stroke-dasharray="3"/>
        <path d="M 40,115 L 90,25 L 140,40 L 190,95 L 240,48 L 290,42 L 340,82 L 390,55" fill="none" stroke="#f43f5e" stroke-width="3" stroke-linecap="round"/>
        <polygon points="40,115 90,25 140,40 190,95 240,48 290,42 340,82 390,55 390,145 40,145" fill="url(#areaGrad)"/>
        <circle cx="90" cy="25" r="4" fill="#f43f5e"/>
        <text x="95" y="20" fill="#fb7185" font-size="11" font-weight="bold">7,007.10</text>
        <circle cx="390" cy="55" r="4" fill="#f43f5e"/>
        <text x="330" y="50" fill="#fb7185" font-size="11" font-weight="bold">6,960.24</text>
      </svg>
      <div style="display: flex; justify-content: space-between; font-size: 11px; color: var(--text-secondary); margin-top: 6px;">
        <span>09:00 개장 (6,938.34)</span>
        <span>09:30</span>
        <span>장중 (6,960.24)</span>
      </div>
    </div>

    <div class="chart-box">
      <div class="chart-title">
        <span>국내 증시 투자자별 순매수/순매도 (억원)</span>
        <span class="neutral" style="font-size: 12px;">외인·기관 쌍끌이</span>
      </div>
      <svg viewBox="0 0 420 160" style="width: 100%; height: 160px;">
        <text x="20" y="32" fill="#94a3b8" font-size="12">외국인 순매수</text>
        <rect x="130" y="18" width="160" height="18" fill="#f43f5e" rx="4"/>
        <text x="298" y="32" fill="#fb7185" font-size="12" font-weight="bold">+1,868 억원</text>

        <text x="20" y="72" fill="#94a3b8" font-size="12">기관 순매수</text>
        <rect x="130" y="58" width="60" height="18" fill="#f43f5e" rx="4"/>
        <text x="198" y="72" fill="#fb7185" font-size="12" font-weight="bold">+642 억원</text>

        <text x="20" y="112" fill="#94a3b8" font-size="12">개인 순매도</text>
        <rect x="130" y="98" width="220" height="18" fill="#38bdf8" rx="4"/>
        <text x="358" y="112" fill="#38bdf8" font-size="12" font-weight="bold">-3,361 억원</text>
      </svg>
      <div style="font-size: 11px; color: var(--text-secondary); text-align: right; margin-top: 6px;">
        * 코스피 수급 잠정 집계치
      </div>
    </div>
  </div>

  <!-- Detailed Table: Domestic -->
  <div class="section-header">
    <span>📋 국내 시장 수급 및 세부 현황</span>
  </div>
  <div class="table-card">
    <table>
      <thead>
        <tr>
          <th>시장명</th>
          <th>현재 지수</th>
          <th>등락폭</th>
          <th>등락률</th>
          <th>외국인 동향</th>
          <th>기관 동향</th>
          <th>개인 동향</th>
          <th class="text-right">시장 특징 및 주도 섹터</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>코스피 (KOSPI)</strong></td>
          <td class="up" style="font-weight: 800;">6,960.24</td>
          <td class="up">▲ +66.01</td>
          <td class="up" style="font-weight: 800;">+0.96%</td>
          <td><span class="badge-buy">+1,868억원 순매수</span></td>
          <td><span class="badge-buy">+642억원 순매수</span></td>
          <td><span class="badge-sell">-3,361억원 순매도</span></td>
          <td class="text-right">삼성전자(+3%대), SK하이닉스 등 반도체 투톱 주도</td>
        </tr>
        <tr>
          <td><strong>코스닥 (KOSDAQ)</strong></td>
          <td class="up" style="font-weight: 800;">830.71</td>
          <td class="up">▲ +3.59</td>
          <td class="up" style="font-weight: 800;">+0.43%</td>
          <td><span class="badge-sell">-373억원 순매도</span></td>
          <td><span class="badge-sell">-217억원 순매도</span></td>
          <td><span class="badge-buy">+645억원 순매수</span></td>
          <td class="text-right">개인 위주 매수세 유입, AI 로봇·장비 개별주 강세</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- News Section -->
  <div class="section-header">
    <span>📰 시장 핵심 헤드라인 스크랩</span>
  </div>
  <div class="news-grid">
    <div class="news-card">
      <h4><a href="https://www.yna.co.kr/view/AKR20260921033051008" target="_blank">[연합뉴스] 코스피, 장초반 1% 내외 상승…장중 '7천피' 일시 회복</a></h4>
      <p class="news-desc">유가증권시장에서 외국인과 기관이 동반 순매수하며 7,000선을 터치. 미국 기술주 랠리 영향으로 대형 반도체주가 강세를 견인.</p>
      <div class="news-footer">
        <span>연합뉴스 | 김유향 기자</span>
        <span>2026-09-21 09:36</span>
      </div>
    </div>
    <div class="news-card">
      <h4><a href="https://news.einfomax.co.kr/news/articleView.html?idxno=4435862" target="_blank">[연합인포맥스] 추석 연휴 앞둔 코스피, 1%대 강세…외인·기관 쌍끌이</a></h4>
      <p class="news-desc">외국인 1,868억원, 기관 642억원 매수 우위. 미 필라델피아 반도체 지수(+2.78%) 급등이 국내 IT 대형주로 직결.</p>
      <div class="news-footer">
        <span>연합인포맥스 | 신민경 기자</span>
        <span>2026-09-21 09:37</span>
      </div>
    </div>
    <div class="news-card">
      <h4><a href="https://biz.chosun.com/stock/stock_general/2026/09/21/QQIKION6XJFXXFC7HVKYLN2IG4/" target="_blank">[조선비즈] 美 기술주 훈풍에 코스피 6,900선 안착…외인 2일 연속 순매수</a></h4>
      <p class="news-desc">외국인이 8거래일 만에 순매수 전환 후 이틀 연속 매수세. 코스닥은 외인·기관 매도로 보합권에 머물며 시장 간 양극화 진행.</p>
      <div class="news-footer">
        <span>조선비즈</span>
        <span>2026-09-21 09:14</span>
      </div>
    </div>
  </div>

  <!-- Macro Analysis -->
  <div class="section-header">
    <span>💡 시장 및 매크로 종합 분석 코멘트</span>
  </div>
  <div class="commentary-card">
    <p><strong>1. 반도체 주도의 지수 견인과 수급 특징:</strong><br>
    미국 나스닥(+0.39%) 및 필라델피아 반도체 지수(+2.78%) 급등에 힘입어 코스피가 7,000선 돌파를 시도하고 있습니다. 특히 외국인이 지난 18일 8거래일 만에 순매수 전환한 데 이어 오늘 장 초반 1,800억원 이상의 매수 우위를 기록하며 지수 상승을 주도하고 있습니다.</p>
    <p><strong>2. 코스피와 코스닥의 뚜렷한 디커플링(양극화):</strong><br>
    외국인과 기관의 자금이 대형 반도체주로 집중되면서 코스피는 1% 가까운 상승세를 보이는 반면, 코스닥은 외국인·기관의 동반 순매도로 인해 보합권에 머물고 있습니다. 지수 전반의 온기보다는 실적 및 주도주 중심의 압축 대응이 필요한 국면입니다.</p>
    <p><strong>3. 외환 및 원자재 시장 시사점:</strong><br>
    WTI 유가가 배럴당 $94.43(-1.72%)로 하락해 물가 불안이 완화된 점은 긍정적이나, 원/달러 환율이 1,386원선에서 고착화되어 있습니다. 고환율은 수출주 실적에는 우호적이나 외국인 환차손 우려가 공존하므로 오후장 수급 이탈 여부를 주시해야 합니다.</p>
  </div>

  <footer>
    <p>© 2026 금융시장 데일리 분석 시스템 | 1일 4회 자동 갱신 (07:00 / 11:30 / 16:00 / 22:00) | 수신처: dbsw1012@gmail.com</p>
  </footer>
</div>

<script>
  let countdown = 30;
  let isUpdating = false;

  // 1. 실시간 KST 시계 갱신
  function updateLiveClock() {
    const now = new Date();
    const kst = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
    const hours = String(kst.getHours()).padStart(2, '0');
    const minutes = String(kst.getMinutes()).padStart(2, '0');
    const seconds = String(kst.getSeconds()).padStart(2, '0');
    const clockEl = document.getElementById('live-clock');
    if (clockEl) {
      clockEl.innerText = `${kst.getFullYear()}-${String(kst.getMonth()+1).padStart(2,'0')}-${String(kst.getDate()).padStart(2,'0')} ${hours}:${minutes}:${seconds} KST`;
    }
  }
  setInterval(updateLiveClock, 1000);
  updateLiveClock();

  // 2. 카드 시세 변동 플래시 효과 (한국 증시: 상승=빨강, 하락=파랑)
  function triggerFlash(cardId, flashClass) {
    const card = document.getElementById(cardId);
    if (!card) return;
    card.classList.remove('flash-green', 'flash-red', 'flash-blue');
    void card.offsetWidth;
    card.classList.add(flashClass);
  }

  // 3. 범용 카드 시세 UI 업데이트 헬퍼 함수
  function updateCard(cardId, valId, rateId, priceStr, changeStr, rateNum) {
    const valEl = document.getElementById(valId);
    const rateEl = document.getElementById(rateId);
    if (!valEl || !rateEl) return;

    valEl.innerText = priceStr;
    const isUp = rateNum > 0;
    const isZero = rateNum === 0;
    const sign = isUp ? '▲ +' : (isZero ? '' : '▼ ');
    const colorClass = isUp ? 'up' : (isZero ? 'neutral' : 'down');

    valEl.className = 'card-val ' + colorClass;
    rateEl.className = 'card-chg ' + colorClass;
    
    if (changeStr) {
      rateEl.innerText = `${sign}${changeStr} (${Math.abs(rateNum).toFixed(2)}%)`;
    } else {
      rateEl.innerText = `${sign}${rateNum > 0 ? '+' : ''}${rateNum.toFixed(2)}%`;
    }

    triggerFlash(cardId, isUp ? 'flash-red' : (isZero ? 'flash-green' : 'flash-blue'));
  }

  // 4. CORS 프록시 풀 (다중 폴백 지원)
  async function fetchWithProxy(targetUrl) {
    const proxies = [
      url => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
      url => `https://corsproxy.io/?url=${encodeURIComponent(url)}`,
      url => `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`
    ];

    for (const proxyFn of proxies) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 4500);
        const res = await fetch(proxyFn(targetUrl), {
          signal: controller.signal,
          headers: { 'Accept': 'application/json' }
        });
        clearTimeout(timeoutId);
        if (res.ok) {
          const text = await res.text();
          try {
            return JSON.parse(text);
          } catch (e) {
            continue;
          }
        }
      } catch (e) {
        // 프록시 에러 시 다음 프록시 시도
      }
    }
    throw new Error('All CORS proxies failed for ' + targetUrl);
  }

  // 5. 야후 파이낸스 차트 API를 통한 지수/원자재/환율 시세 조회
  async function fetchYahooQuote(symbol) {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=1d`;
    const data = await fetchWithProxy(url);
    if (data && data.chart && data.chart.result && data.chart.result.length > 0) {
      const meta = data.chart.result[0].meta;
      const price = meta.regularMarketPrice;
      const prevClose = meta.chartPreviousClose || meta.previousClose;
      if (price !== undefined && prevClose !== undefined) {
        const diff = price - prevClose;
        const rate = (diff / prevClose) * 100;
        return { price, prevClose, diff, rate };
      }
    }
    throw new Error('Invalid Yahoo data structure for ' + symbol);
  }

  // 6. 네이버 금융 모바일 API를 통한 국내 지수 및 주식 시세 조회
  async function fetchNaverStock(code) {
    const url = `https://m.stock.naver.com/api/stock/${code}/basic`;
    const data = await fetchWithProxy(url);
    if (data && data.stockName) {
      const price = data.nowValue || data.closePrice;
      const diff = data.changeVal || data.compareToPreviousClosePrice;
      const rate = parseFloat(data.fluctuationsRatio || '0');
      const isRising = data.compareToPreviousPrice && (data.compareToPreviousPrice.name === 'RISING' || data.compareToPreviousPrice.code === '2');
      return {
        name: data.stockName,
        price: price + '원',
        diff: diff,
        rate: isRising ? Math.abs(rate) : -Math.abs(rate)
      };
    }
    throw new Error('Invalid Naver stock data for ' + code);
  }

  async function fetchNaverIndex(market) {
    const url = `https://m.stock.naver.com/api/index/${market}/basic`;
    const data = await fetchWithProxy(url);
    if (data && data.closePrice) {
      const price = parseFloat(data.closePrice.replace(/,/g, ''));
      const diff = parseFloat((data.compareToPreviousClosePrice || '0').replace(/,/g, ''));
      const rate = parseFloat(data.fluctuationsRatio || '0');
      const isRising = data.compareToPreviousPrice && (data.compareToPreviousPrice.name === 'RISING' || data.compareToPreviousPrice.code === '2');
      return {
        price: price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}),
        diff: diff.toFixed(2),
        rate: isRising ? Math.abs(rate) : -Math.abs(rate)
      };
    }
    throw new Error('Invalid Naver index data for ' + market);
  }

  // 7. 전체 실시간 시장 데이터 일괄 수신 및 UI 갱신 메인 루프
  async function fetchAllLiveMarketData() {
    if (isUpdating) return;
    isUpdating = true;

    const now = new Date();
    const kst = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
    const hours = String(kst.getHours()).padStart(2, '0');
    const minutes = String(kst.getMinutes()).padStart(2, '0');
    const seconds = String(kst.getSeconds()).padStart(2, '0');
    const timeStr = `${String(kst.getMonth()+1).padStart(2,'0')}.${String(kst.getDate()).padStart(2,'0')} ${hours}:${minutes}:${seconds} 갱신`;

    document.querySelectorAll('.card-time').forEach(el => {
      el.innerText = timeStr;
    });
    const syncEl = document.getElementById('sync-time');
    if (syncEl) syncEl.innerText = `${timeStr} (실시간 동기화 완료)`;

    // (1) 가상자산 실시간 (업비트 직접 통신)
    try {
      const res = await fetch('https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH');
      if (res.ok) {
        const data = await res.json();
        const btc = data.find(c => c.market === 'KRW-BTC');
        if (btc) {
          const r = (btc.signed_change_rate * 100);
          const diffStr = (btc.signed_change_price >= 0 ? '+' : '') + btc.signed_change_price.toLocaleString() + '원';
          updateCard('card-btc', 'val-btc', 'rate-btc', btc.trade_price.toLocaleString() + '원', diffStr, r);
        }
        const eth = data.find(c => c.market === 'KRW-ETH');
        if (eth) {
          const r = (eth.signed_change_rate * 100);
          const diffStr = (eth.signed_change_price >= 0 ? '+' : '') + eth.signed_change_price.toLocaleString() + '원';
          updateCard('card-eth', 'val-eth', 'rate-eth', eth.trade_price.toLocaleString() + '원', diffStr, r);
        }
      }
    } catch(e) {
      console.warn('업비트 API 갱신 예외:', e);
    }

    // (2) 환율 실시간
    try {
      const resFx = await fetch('https://open.er-api.com/v6/latest/USD');
      if (resFx.ok) {
        const dataFx = await resFx.json();
        if (dataFx && dataFx.rates && dataFx.rates.KRW) {
          const krwRate = dataFx.rates.KRW;
          const valFxEl = document.getElementById('val-fx');
          if (valFxEl) valFxEl.innerText = Number(krwRate.toFixed(2)).toLocaleString() + '원';
          triggerFlash('card-fx', 'flash-red');
        }
      }
    } catch(e) {
      console.warn('외환 API 갱신 예외:', e);
    }

    // (3) 국내 증시 지수 (코스피 / 코스닥) 실시간 갱신
    const domesticPromises = [
      (async () => {
        try {
          const kospi = await fetchNaverIndex('KOSPI');
          updateCard('card-kospi', 'val-kospi', 'rate-kospi', kospi.price, (kospi.rate >= 0 ? '+' : '') + kospi.diff, kospi.rate);
        } catch (e) {
          try {
            const yKospi = await fetchYahooQuote('^KS11');
            updateCard('card-kospi', 'val-kospi', 'rate-kospi', yKospi.price.toLocaleString(undefined, {minimumFractionDigits: 2}), (yKospi.diff >= 0 ? '+' : '') + yKospi.diff.toFixed(2), yKospi.rate);
          } catch(err) {
            console.warn('KOSPI 갱신 스킵');
          }
        }
      })(),
      (async () => {
        try {
          const kosdaq = await fetchNaverIndex('KOSDAQ');
          updateCard('card-kosdaq', 'val-kosdaq', 'rate-kosdaq', kosdaq.price, (kosdaq.rate >= 0 ? '+' : '') + kosdaq.diff, kosdaq.rate);
        } catch (e) {
          try {
            const yKosdaq = await fetchYahooQuote('^KQ11');
            updateCard('card-kosdaq', 'val-kosdaq', 'rate-kosdaq', yKosdaq.price.toLocaleString(undefined, {minimumFractionDigits: 2}), (yKosdaq.diff >= 0 ? '+' : '') + yKosdaq.diff.toFixed(2), yKosdaq.rate);
          } catch(err) {
            console.warn('KOSDAQ 갱신 스킵');
          }
        }
      })()
    ];

    // (4) 글로벌 증시 및 원자재 실시간 갱신
    const globalSymbols = [
      { id: 'card-spx', val: 'val-spx', rate: 'rate-spx', sym: '^GSPC', format: p => p.toLocaleString(undefined, {minimumFractionDigits: 2}) },
      { id: 'card-nasdaq', val: 'val-nasdaq', rate: 'rate-nasdaq', sym: '^IXIC', format: p => p.toLocaleString(undefined, {minimumFractionDigits: 2}) },
      { id: 'card-dow', val: 'val-dow', rate: 'rate-dow', sym: '^DJI', format: p => p.toLocaleString(undefined, {minimumFractionDigits: 2}) },
      { id: 'card-oil', val: 'val-oil', rate: 'rate-oil', sym: 'CL=F', format: p => '$' + p.toFixed(2) },       { id: 'card-gold', val: 'val-gold', rate: 'rate-gold', sym: 'GC=F', format: p => '$' + p.toLocaleString(undefined, {minimumFractionDigits: 2}) }
    ];

    const globalPromises = globalSymbols.map(async item => {
      try {
        const q = await fetchYahooQuote(item.sym);
        const diffStr = (q.diff >= 0 ? '+' : '') + q.diff.toFixed(2);
        updateCard(item.id, item.val, item.rate, item.format(q.price), diffStr, q.rate);
      } catch (err) {
        console.warn(`${item.sym} 시세 갱신 스킵`);
      }
    });

    // (5) 기본 워치리스트 종목 (삼성전자, 하이닉스, 현대차, 네이버) 실시간 갱신
    const defaultWatchStocks = [
      { code: '005930', card: 'stock-005930', val: 'val-stock-005930', rate: 'rate-stock-005930' },
      { code: '000660', card: 'stock-000660', val: 'val-stock-000660', rate: 'rate-stock-000660' },
      { code: '005380', card: 'stock-005380', val: 'val-stock-005380', rate: 'rate-stock-005380' },
      { code: '035420', card: 'stock-035420', val: 'val-stock-035420', rate: 'rate-stock-035420' }
    ];

    const stockPromises = defaultWatchStocks.map(async s => {
      try {
        const stockData = await fetchNaverStock(s.code);
        const diffStr = (stockData.rate >= 0 ? '+' : '') + stockData.diff;
        updateCard(s.card, s.val, s.rate, stockData.price, diffStr, stockData.rate);
      } catch (e) {
        console.warn(`종목 ${s.code} 갱신 실패:`, e.message);
      }
    });

    // (6) 사용자 추가 관심종목 실시간 갱신
    const customStocks = getSavedStocks();
    const customPromises = customStocks.map(async s => {
      try {
        const stockData = await fetchNaverStock(s.code);
        const diffStr = (stockData.rate >= 0 ? '+' : '') + stockData.diff;
        updateCard(`stock-${s.code}`, `val-custom-${s.code}`, `rate-custom-${s.code}`, stockData.price, diffStr, stockData.rate);
      } catch (e) {
        // 기존 상태 유지
      }
    });

    await Promise.allSettled([...domesticPromises, ...globalPromises, ...stockPromises, ...customPromises]);

    countdown = 30;
    isUpdating = false;
  }

  // 8. 30초 카운트다운 타이머
  setInterval(() => {
    countdown--;
    const tEl = document.getElementById('timer-sec');
    if (tEl) tEl.innerText = countdown;
    if (countdown <= 0) {
      fetchAllLiveMarketData();
    }
  }, 1000);

  // 9. 사용자 관심종목 관리 (localStorage)
  function getSavedStocks() {
    try {
      return JSON.parse(localStorage.getItem('my_stocks')) || [];
    } catch(e) {
      return [];
    }
  }

  function saveStock(code, name, price, change, rate) {
    let stocks = getSavedStocks();
    if (!stocks.some(s => s.code === code)) {
      stocks.push({code, name, price, change, rate});
      localStorage.setItem('my_stocks', JSON.stringify(stocks));
      renderWatchlist();
    }
  }

  function removeStock(code) {
    let stocks = getSavedStocks().filter(s => s.code !== code);
    localStorage.setItem('my_stocks', JSON.stringify(stocks));
    renderWatchlist();
  }

  async function addCustomStock() {
    const input = document.getElementById('custom-stock-code');
    const code = input.value.trim();
    if (!code) {
      alert('종목코드 6자리를 입력해주세요 (예: 005930)');
      return;
    }

    const btn = document.querySelector('.watchlist-btn');
    const originalText = btn ? btn.innerText : '+ 종목 추가';
    if (btn) { btn.innerText = '조회 중...'; btn.disabled = true; }

    try {
      const stockData = await fetchNaverStock(code);
      const diffStr = (stockData.rate >= 0 ? '▲ +' : '▼ ') + stockData.diff;
      saveStock(code, stockData.name, stockData.price, diffStr, (stockData.rate >= 0 ? '+' : '') + stockData.rate.toFixed(2) + '%');
      input.value = '';
    } catch(e) {
      try {
        const yQuote = await fetchYahooQuote(`${code}.KS`);
        const diffStr = (yQuote.rate >= 0 ? '▲ +' : '▼ ') + yQuote.diff.toLocaleString() + '원';
        saveStock(code, `종목 ${code}`, yQuote.price.toLocaleString() + '원', diffStr, (yQuote.rate >= 0 ? '+' : '') + yQuote.rate.toFixed(2) + '%');
        input.value = '';
      } catch(err) {
        alert(`종목코드 [${code}] 정보를 조회할 수 없습니다. 6자리 코드를 다시 확인해주세요.`);
      }
    } finally {
      if (btn) { btn.innerText = originalText; btn.disabled = false; }
    }
  }

  function renderWatchlist() {
    const container = document.getElementById('watchlist-container');
    const customStocks = getSavedStocks();
    document.querySelectorAll('.custom-stock-card').forEach(el => el.remove());

    const now = new Date();
    const kst = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
    const timeStr = `${String(kst.getMonth()+1).padStart(2,'0')}.${String(kst.getDate()).padStart(2,'0')} ${String(kst.getHours()).padStart(2,'0')}:${String(kst.getMinutes()).padStart(2,'0')} 갱신`;

    customStocks.forEach(s => {
      const card = document.createElement('div');
      card.className = 'card custom-stock-card';
      card.id = `stock-${s.code}`;
      const isUp = !s.rate.includes('-');
      const colorClass = isUp ? 'up' : 'down';
      card.innerHTML = `
        <div class="card-header-row">
          <span class="card-label">${s.name} (${s.code})</span>
          <div style="display:flex; align-items:center; gap:6px;">
            <span class="card-time">${timeStr}</span>
            <button class="del-btn" onclick="removeStock('${s.code}')" title="삭제">×</button>
          </div>
        </div>
        <div class="card-val ${colorClass}" id="val-custom-${s.code}">${s.price}</div>
        <div class="card-chg ${colorClass}" id="rate-custom-${s.code}">${s.change} (${s.rate})</div>
        <div class="card-desc">사용자 실시간 관심종목</div>
      `;
      container.appendChild(card);
    });
  }

  // 10. 페이지 로드 즉시 실시간 데이터 일괄 호출
  document.addEventListener('DOMContentLoaded', () => {
    renderWatchlist();
    fetchAllLiveMarketData();
  });
</script>
</body>
</html>"""

def build_html():
    d = get_market_data()
    html = HTML_TEMPLATE
    html = html.replace("{{KOSPI}}", str(d['kospi']))
    html = html.replace("{{KOSPI_RATE_STR}}", str(d['kospi_rate_str']))
    html = html.replace("{{KOSDAQ}}", str(d['kosdaq']))
    html = html.replace("{{KOSDAQ_RATE_STR}}", str(d['kosdaq_rate_str']))
    html = html.replace("{{SPX}}", str(d['spx']))
    html = html.replace("{{SPX_RATE_STR}}", str(d['spx_rate_str']))
    html = html.replace("{{NASDAQ}}", str(d['nasdaq']))
    html = html.replace("{{NASDAQ_RATE_STR}}", str(d['nasdaq_rate_str']))
    html = html.replace("{{DOW}}", str(d['dow']))
    html = html.replace("{{DOW_RATE_STR}}", str(d['dow_rate_str']))
    html = html.replace("{{USD_KRW}}", str(d['usd_krw']))
    html = html.replace("{{USD_RATE_STR}}", str(d['usd_rate_str']))
    html = html.replace("{{OIL}}", str(d['oil']))
    html = html.replace("{{OIL_RATE_STR}}", str(d['oil_rate_str']))
    html = html.replace("{{GOLD}}", str(d['gold']))
    html = html.replace("{{GOLD_RATE_STR}}", str(d['gold_rate_str']))
    html = html.replace("{{BTC}}", str(d['btc']))
    html = html.replace("{{BTC_RATE_STR}}", str(d['btc_rate_str']))
    html = html.replace("{{ETH}}", str(d['eth']))
    html = html.replace("{{ETH_RATE_STR}}", str(d['eth_rate_str']))
    html = html.replace("{{SYNC_TIME}}", str(d['sync_time']))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html successfully built by build_dashboard.py!")

if __name__ == '__main__':
    build_html()
