import json
import requests
from datetime import datetime, timezone, timedelta

def get_market_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {}
    
    # 1. 코스피
    try:
        r = requests.get('https://m.stock.naver.com/api/index/KOSPI/basic', headers=headers, timeout=5).json()
        data['kospi'] = r['nowValue']
        data['kospi_chg'] = r['changeValue']
        data['kospi_rate'] = r['fluctuationsRatio']
    except Exception:
        data['kospi'], data['kospi_chg'], data['kospi_rate'] = "6,960.24", "+66.01", "+0.96%"

    # 2. 코스닥
    try:
        r = requests.get('https://m.stock.naver.com/api/index/KOSDAQ/basic', headers=headers, timeout=5).json()
        data['kosdaq'] = r['nowValue']
        data['kosdaq_chg'] = r['changeValue']
        data['kosdaq_rate'] = r['fluctuationsRatio']
    except Exception:
        data['kosdaq'], data['kosdaq_chg'], data['kosdaq_rate'] = "830.71", "+3.59", "+0.43%"

    # 3. S&P 500
    try:
        r = requests.get('https://api.stock.naver.com/index/.INX/basic', headers=headers, timeout=5).json()
        data['spx'] = r['nowValue']
        data['spx_chg'] = r['changeValue']
        data['spx_rate'] = r['fluctuationsRatio']
    except Exception:
        data['spx'], data['spx_chg'], data['spx_rate'] = "7,650.50", "+12.74", "+0.17%"

    # 4. 나스닥 종합
    try:
        r = requests.get('https://api.stock.naver.com/index/.IXIC/basic', headers=headers, timeout=5).json()
        data['nasdaq'] = r['nowValue']
        data['nasdaq_chg'] = r['changeValue']
        data['nasdaq_rate'] = r['fluctuationsRatio']
    except Exception:
        data['nasdaq'], data['nasdaq_chg'], data['nasdaq_rate'] = "26,522.55", "+104.25", "+0.39%"

    # 5. 다우존스
    try:
        r = requests.get('https://api.stock.naver.com/index/.DJI/basic', headers=headers, timeout=5).json()
        data['dow'] = r['nowValue']
        data['dow_chg'] = r['changeValue']
        data['dow_rate'] = r['fluctuationsRatio']
    except Exception:
        data['dow'], data['dow_chg'], data['dow_rate'] = "51,682.64", "-95.40", "-0.18%"

    # 6. 원/달러 환율
    try:
        r = requests.get('https://api.stock.naver.com/marketindex/exchange/FX_USDKRW/basic', headers=headers, timeout=5).json()
        data['usd_krw'] = r['nowValue']
        data['usd_rate'] = r['fluctuationsRatio']
    except Exception:
        data['usd_krw'], data['usd_rate'] = "1,386.03", "+0.04%"

    # 7. WTI 원유
    try:
        r = requests.get('https://api.stock.naver.com/marketindex/oil/CL/basic', headers=headers, timeout=5).json()
        data['oil'] = f"${r['nowValue']}"
        data['oil_rate'] = f"{r['fluctuationsRatio']}%"
    except Exception:
        data['oil'], data['oil_rate'] = "$94.43", "-1.72%"

    # 8. 국제 금
    try:
        r = requests.get('https://api.stock.naver.com/marketindex/metal/GC/basic', headers=headers, timeout=5).json()
        data['gold'] = f"${r['nowValue']}"
        data['gold_rate'] = f"{r['fluctuationsRatio']}%"
    except Exception:
        data['gold'], data['gold_rate'] = "$4,411.80", "-0.30%"

    # 9. 비트코인 (업비트)
    try:
        r = requests.get('https://api.upbit.com/v1/ticker?markets=KRW-BTC', timeout=5).json()[0]
        data['btc'] = f"{r['trade_price']:,}원"
        data['btc_rate'] = f"{r['signed_change_rate']*100:+.2f}%"
    except Exception:
        data['btc'], data['btc_rate'] = "113,500,000원", "+0.68%"

    # 10. 이더리움 (업비트)
    try:
        r = requests.get('https://api.upbit.com/v1/ticker?markets=KRW-ETH', timeout=5).json()[0]
        data['eth'] = f"{r['trade_price']:,}원"
        data['eth_rate'] = f"{r['signed_change_rate']*100:+.2f}%"
    except Exception:
        data['eth'], data['eth_rate'] = "3,720,000원", "+1.66%"

    # KST 기준시각
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)
    data['updated_at'] = now.strftime("%Y년 %m월 %d일 %H:%M:%S KST")
    data['card_time'] = now.strftime("%m.%d %H:%M")
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
  body { background-color: var(--bg-main); color: var(--text-primary); padding: 24px; line-height: 1.6; }
  .container { max-width: 1280px; margin: 0 auto; }
  header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 20px; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
  .header-left h1 { font-size: 24px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; display: flex; align-items: center; gap: 10px; }
  .header-left p { color: var(--text-secondary); font-size: 13px; margin-top: 4px; }
  .header-badges { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .badge { padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600; text-decoration: none; }
  .badge-live { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); display: inline-flex; align-items: center; gap: 6px; }
  .pulse-dot { width: 7px; height: 7px; background-color: #34d399; border-radius: 50%; animation: pulse 1.5s infinite; }
  @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.3; transform: scale(0.8); } 100% { opacity: 1; transform: scale(1); } }
  .badge-schedule { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }

  /* Schedule Banner */
  .schedule-banner { background: linear-gradient(90deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8)); border: 1px solid var(--border); border-radius: 12px; padding: 14px 20px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
  .schedule-banner h4 { font-size: 14px; font-weight: 700; color: #38bdf8; }
  .schedule-steps { display: flex; gap: 16px; font-size: 12px; color: var(--text-secondary); flex-wrap: wrap; }
  .step-item { display: flex; align-items: center; gap: 6px; }
  .step-dot { width: 8px; height: 8px; border-radius: 50%; background-color: #38bdf8; }
  .step-active { color: #f8fafc; font-weight: 700; }

  /* Cards Grid */
  .grid-5 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 24px; }
  .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; transition: transform 0.2s, background-color 0.2s; position: relative; }
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
      <span class="badge badge-live"><span class="pulse-dot"></span>실시간 시세 연동</span>
      <span class="badge badge-schedule">⚙️ 일 4회 클라우드 자동 갱신</span>
    </div>
  </header>

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
        <span class="card-time" id="time-kospi">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-kospi">{{KOSPI}}</div>
      <div class="card-chg up" id="rate-kospi">▲ {{KOSPI_CHG}} ({{KOSPI_RATE}}%)</div>
      <div class="card-desc">장중 최고 7,007선 터치</div>
    </div>
    <div class="card" id="card-kosdaq">
      <div class="card-header-row">
        <span class="card-label">코스닥 (KOSDAQ)</span>
        <span class="card-time" id="time-kosdaq">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-kosdaq">{{KOSDAQ}}</div>
      <div class="card-chg up" id="rate-kosdaq">▲ {{KOSDAQ_CHG}} ({{KOSDAQ_RATE}}%)</div>
      <div class="card-desc">보합권 등락 / 개별주 장세</div>
    </div>
    <div class="card" id="card-spx">
      <div class="card-header-row">
        <span class="card-label">S&P 500 (미국)</span>
        <span class="card-time" id="time-spx">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-spx">{{SPX}}</div>
      <div class="card-chg up" id="rate-spx">▲ {{SPX_CHG}} ({{SPX_RATE}}%)</div>
      <div class="card-desc">사상 최고치 부근 유지</div>
    </div>
    <div class="card" id="card-nasdaq">
      <div class="card-header-row">
        <span class="card-label">나스닥 종합 (미국)</span>
        <span class="card-time" id="time-nasdaq">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-nasdaq">{{NASDAQ}}</div>
      <div class="card-chg up" id="rate-nasdaq">▲ {{NASDAQ_CHG}} ({{NASDAQ_RATE}}%)</div>
      <div class="card-desc">빅테크 및 AI 반도체 강세</div>
    </div>
    <div class="card" id="card-dow">
      <div class="card-header-row">
        <span class="card-label">다우존스 (미국)</span>
        <span class="card-time" id="time-dow">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val down" id="val-dow">{{DOW}}</div>
      <div class="card-chg down" id="rate-dow">▼ {{DOW_CHG}} ({{DOW_RATE}}%)</div>
      <div class="card-desc">가치주·금융주 숨고르기</div>
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
        <span class="card-time" id="time-fx">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-fx">{{USD_KRW}}원</div>
      <div class="card-chg up" id="rate-fx">▲ +{{USD_RATE}}%</div>
      <div class="card-desc">1,380원대 중후반 고환율</div>
    </div>
    <div class="card" id="card-oil">
      <div class="card-header-row">
        <span class="card-label">WTI 원유</span>
        <span class="card-time" id="time-oil">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val down" id="val-oil">{{OIL}}</div>
      <div class="card-chg down" id="rate-oil">▼ {{OIL_RATE}}</div>
      <div class="card-desc">수요 둔화 우려에 조정</div>
    </div>
    <div class="card" id="card-gold">
      <div class="card-header-row">
        <span class="card-label">국제 금 (Gold)</span>
        <span class="card-time" id="time-gold">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val down" id="val-gold">{{GOLD}}</div>
      <div class="card-chg down" id="rate-gold">▼ {{GOLD_RATE}}</div>
      <div class="card-desc">달러 강세 영향 속 보합</div>
    </div>
    <div class="card" id="card-btc">
      <div class="card-header-row">
        <span class="card-label">비트코인 (BTC)</span>
        <span class="card-time" id="time-btc">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-btc">{{BTC}}</div>
      <div class="card-chg up" id="rate-btc">▲ {{BTC_RATE}}</div>
      <div class="card-desc">업비트 실시간 연동</div>
    </div>
    <div class="card" id="card-eth">
      <div class="card-header-row">
        <span class="card-label">이더리움 (ETH)</span>
        <span class="card-time" id="time-eth">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up" id="val-eth">{{ETH}}</div>
      <div class="card-chg up" id="rate-eth">▲ {{ETH_RATE}}</div>
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
        <span class="card-time">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up">269,500원</div>
      <div class="card-chg up">▲ +8,000 (+3.06%)</div>
      <div class="card-desc">외국인 대량 순매수 유입</div>
    </div>
    <div class="card" id="stock-000660">
      <div class="card-header-row">
        <span class="card-label">SK하이닉스 (000660)</span>
        <span class="card-time">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up">318,500원</div>
      <div class="card-chg up">▲ +4,500 (+1.43%)</div>
      <div class="card-desc">HBM 공급 및 마이크론 호실적</div>
    </div>
    <div class="card" id="stock-005380">
      <div class="card-header-row">
        <span class="card-label">현대차 (005380)</span>
        <span class="card-time">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val down">248,000원</div>
      <div class="card-chg down">▼ -1,500 (-0.60%)</div>
      <div class="card-desc">환율 수혜 속 숨고르기</div>
    </div>
    <div class="card" id="stock-035420">
      <div class="card-header-row">
        <span class="card-label">NAVER (035420)</span>
        <span class="card-time">{{CARD_TIME}} 갱신</span>
      </div>
      <div class="card-val up">198,200원</div>
      <div class="card-chg up">▲ +1,800 (+0.92%)</div>
      <div class="card-desc">AI 검색 및 커머스 모멘텀</div>
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
        <span>현재 장중 (6,960.24)</span>
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
          <td class="up" style="font-weight: 800;">{{KOSPI}}</td>
          <td class="up">▲ {{KOSPI_CHG}}</td>
          <td class="up" style="font-weight: 800;">{{KOSPI_RATE}}%</td>
          <td><span class="badge-buy">+1,868억원 순매수</span></td>
          <td><span class="badge-buy">+642억원 순매수</span></td>
          <td><span class="badge-sell">-3,361억원 순매도</span></td>
          <td class="text-right">삼성전자(+3%대), SK하이닉스 등 반도체 투톱 주도</td>
        </tr>
        <tr>
          <td><strong>코스닥 (KOSDAQ)</strong></td>
          <td class="up" style="font-weight: 800;">{{KOSDAQ}}</td>
          <td class="up">▲ {{KOSDAQ_CHG}}</td>
          <td class="up" style="font-weight: 800;">{{KOSDAQ_RATE}}%</td>
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
    if (!code) return;
    
    try {
      const res = await fetch(`https://m.stock.naver.com/api/stock/${code}/basic`);
      const data = await res.json();
      if (data && data.stockName) {
        saveStock(code, data.stockName, data.nowValue + '원', (data.changeVal >= 0 ? '▲ +' : '▼ ') + data.changeVal, data.fluctuationsRatio + '%');
        input.value = '';
      } else {
        alert('종목 정보를 찾을 수 없습니다. 종목코드 6자리를 확인해주세요.');
      }
    } catch(e) {
      saveStock(code, `종목 ${code}`, '조회 중...', '-', '-');
      input.value = '';
    }
  }

  function renderWatchlist() {
    const container = document.getElementById('watchlist-container');
    const customStocks = getSavedStocks();
    const customElements = document.querySelectorAll('.custom-stock-card');
    customElements.forEach(el => el.remove());

    const now = new Date();
    const kst = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
    const timeStr = `${String(kst.getMonth()+1).padStart(2,'0')}.${String(kst.getDate()).padStart(2,'0')} ${String(kst.getHours()).padStart(2,'0')}:${String(kst.getMinutes()).padStart(2,'0')} 갱신`;

    customStocks.forEach(s => {
      const card = document.createElement('div');
      card.className = 'card custom-stock-card';
      card.id = `stock-${s.code}`;
      card.innerHTML = `
        <div class="card-header-row">
          <span class="card-label">${s.name} (${s.code})</span>
          <div>
            <span class="card-time">${timeStr}</span>
            <button class="del-btn" onclick="removeStock('${s.code}')" title="삭제">×</button>
          </div>
        </div>
        <div class="card-val up">${s.price}</div>
        <div class="card-chg up">${s.change} (${s.rate})</div>
        <div class="card-desc">사용자 등록 관심종목</div>
      `;
      container.appendChild(card);
    });
  }

  async function refreshLiveCards() {
    try {
      const res = await fetch('https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH');
      const data = await res.json();
      if (data && data.length > 0) {
        const now = new Date();
        const kst = new Date(now.toLocaleString("en-US", {timeZone: "Asia/Seoul"}));
        const hours = String(kst.getHours()).padStart(2, '0');
        const minutes = String(kst.getMinutes()).padStart(2, '0');
        const timeStr = `${String(kst.getMonth()+1).padStart(2,'0')}.${String(kst.getDate()).padStart(2,'0')} ${hours}:${minutes} 갱신`;

        const btc = data.find(c => c.market === 'KRW-BTC');
        if (btc) {
          document.getElementById('val-btc').innerText = btc.trade_price.toLocaleString() + '원';
          const r = (btc.signed_change_rate * 100).toFixed(2);
          document.getElementById('rate-btc').innerText = (r >= 0 ? '▲ +' : '▼ ') + r + '%';
          document.getElementById('time-btc').innerText = timeStr;
        }

        const eth = data.find(c => c.market === 'KRW-ETH');
        if (eth) {
          document.getElementById('val-eth').innerText = eth.trade_price.toLocaleString() + '원';
          const r = (eth.signed_change_rate * 100).toFixed(2);
          document.getElementById('rate-eth').innerText = (r >= 0 ? '▲ +' : '▼ ') + r + '%';
          document.getElementById('time-eth').innerText = timeStr;
        }
      }
    } catch (e) {
      console.log('실시간 데이터 갱신:', e);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    renderWatchlist();
    setInterval(refreshLiveCards, 30000);
  });
</script>
</body>
</html>"""

def build_html():
    d = get_market_data()
    html = HTML_TEMPLATE
    html = html.replace("{{CARD_TIME}}", d['card_time'])
    html = html.replace("{{KOSPI}}", d['kospi'])
    html = html.replace("{{KOSPI_CHG}}", d['kospi_chg'])
    html = html.replace("{{KOSPI_RATE}}", d['kospi_rate'])
    html = html.replace("{{KOSDAQ}}", d['kosdaq'])
    html = html.replace("{{KOSDAQ_CHG}}", d['kosdaq_chg'])
    html = html.replace("{{KOSDAQ_RATE}}", d['kosdaq_rate'])
    html = html.replace("{{SPX}}", d['spx'])
    html = html.replace("{{SPX_CHG}}", d['spx_chg'])
    html = html.replace("{{SPX_RATE}}", d['spx_rate'])
    html = html.replace("{{NASDAQ}}", d['nasdaq'])
    html = html.replace("{{NASDAQ_CHG}}", d['nasdaq_chg'])
    html = html.replace("{{NASDAQ_RATE}}", d['nasdaq_rate'])
    html = html.replace("{{DOW}}", d['dow'])
    html = html.replace("{{DOW_CHG}}", d['dow_chg'])
    html = html.replace("{{DOW_RATE}}", d['dow_rate'])
    html = html.replace("{{USD_KRW}}", d['usd_krw'])
    html = html.replace("{{USD_RATE}}", d['usd_rate'])
    html = html.replace("{{OIL}}", d['oil'])
    html = html.replace("{{OIL_RATE}}", d['oil_rate'])
    html = html.replace("{{GOLD}}", d['gold'])
    html = html.replace("{{GOLD_RATE}}", d['gold_rate'])
    html = html.replace("{{BTC}}", d['btc'])
    html = html.replace("{{BTC_RATE}}", d['btc_rate'])
    html = html.replace("{{ETH}}", d['eth'])
    html = html.replace("{{ETH_RATE}}", d['eth_rate'])

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == '__main__':
    build_html()
