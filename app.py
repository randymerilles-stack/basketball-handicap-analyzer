import os, json, time, math, itertools, urllib.request, datetime
from flask import Flask, jsonify, send_from_directory
app = Flask(__name__, static_folder='.')
SOURCE = 'https://1xbetjap.com/en/live/basketball'
CACHE = {'at': 0, 'data': None}

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def number(x):
    try:
        y = float(x)
        return y if math.isfinite(y) else None
    except (ValueError, TypeError): return None

def normalize(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get('games'), list):
        raise ValueError('Feed must be JSON object with games array')
    out=[]; rejected=0
    for g in payload['games'][:500]:
        try:
            if not isinstance(g,dict): raise ValueError()
            gid=str(g['id']).strip(); league=str(g['league']).strip(); a=str(g['home']).strip(); b=str(g['away']).strip()
            if not all((gid,league,a,b)) or a==b: raise ValueError()
            clock=str(g.get('clock','')); period=str(g.get('period',''))
            hs=number(g.get('home_score')); aws=number(g.get('away_score'))
            if hs is not None and (hs<0 or not hs.is_integer()): raise ValueError()
            if aws is not None and (aws<0 or not aws.is_integer()): raise ValueError()
            selections=[]
            for s in g.get('handicaps',[])[:60]:
                if not isinstance(s,dict): continue
                side=s.get('side'); line=number(s.get('line')); odds=number(s.get('odds'))
                if side not in ('home','away') or line is None or odds is None or odds<=1 or abs(line)>150: continue
                selections.append({'side':side,'team':a if side=='home' else b,'line':line,'odds':odds,'break_even':round(1/odds,4)})
            if selections: out.append({'id':gid,'league':league,'home':a,'away':b,'home_score':hs,'away_score':aws,'period':period,'clock':clock,'handicaps':selections})
            else: rejected+=1
        except (ValueError,TypeError,KeyError): rejected+=1
    return out,rejected

def combinations(games):
    # No real-money betting picks until calibrated cover probabilities exist.
    # Merely compute market break-even numbers; these are NOT win estimates.
    return {'status':'NO MULTI','reason':'No independently validated spread-cover probability model is configured.', 'two_leg_candidates':[], 'three_leg_candidates':[]}

def get_feed():
    url=os.environ.get('MARKET_FEED_URL','').strip()
    if not url: return {'status':'not_configured','games':[], 'message':'No licensed structured Full Game Handicap feed configured.'}
    if not url.startswith('https://'): return {'status':'invalid_configuration','games':[], 'message':'MARKET_FEED_URL must use HTTPS.'}
    if CACHE['data'] is not None and time.time()-CACHE['at']<30: return CACHE['data']
    try:
        req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'HandicapMultiLab/1.6'})
        with urllib.request.urlopen(req,timeout=10) as resp:
            if resp.status!=200: raise ValueError('Feed HTTP '+str(resp.status))
            raw=resp.read(2_000_001)
            if len(raw)>2_000_000: raise ValueError('Feed exceeds size limit')
            payload=json.loads(raw)
        games,rejected=normalize(payload)
        result={'status':'connected','games':games,'rejected':rejected,'message':f'{len(games)} games with valid handicap markets received.'}
        CACHE.update(at=time.time(),data=result)
        return result
    except Exception as e:
        return {'status':'feed_error','games':[],'message':f'Feed unavailable or invalid: {type(e).__name__}'}

@app.get('/')
def home(): return send_from_directory('.', 'index.html')
@app.get('/health')
def health(): return jsonify(ok=True,version='1.6')
@app.get('/api/status')
def status():
    feed=get_feed()
    return jsonify({'checked_at':now(),'source_reference':SOURCE,'version':'1.6','market':'Basketball Full Game Handicap','feed_status':feed['status'],'message':feed['message'],'verified_live_games':feed['games'],'rejected_games':feed.get('rejected',0),'multi':combinations(feed['games']),'refresh_seconds':30})

if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT','10000')))
