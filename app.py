import os, json, urllib.request, urllib.error, datetime
from flask import Flask, jsonify, send_from_directory
app=Flask(__name__,static_folder='.')
SOURCE='https://1xbetjap.com/en/live/basketball'
@app.get('/')
def home(): return send_from_directory('.', 'index.html')
@app.get('/api/status')
def status():
    result={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':SOURCE,'market':'Full Game Handicap','verified_live_games':[],'multi':'NO MULTI','connection':'not_verified','message':'No authorised structured live handicap feed configured.'}
    try:
        req=urllib.request.Request(SOURCE,headers={'User-Agent':'Mozilla/5.0 (compatible; MarketDiagnostics/1.0)'})
        with urllib.request.urlopen(req,timeout=8) as response:
            sample=response.read(4096)
            result['http_status']=response.status
            result['response_type']=response.headers.get('Content-Type','unknown')
            result['bytes_sampled']=len(sample)
            result['connection']='public_page_reachable'
            result['message']='Public page reachable, but no verified structured handicap market feed. NO MULTI.'
    except Exception as e:
        result['connection']='public_page_unreachable'
        result['message']=f'Public page fetch failed: {type(e).__name__}. No market data.'
    return jsonify(result)
@app.get('/health')
def health(): return jsonify(ok=True)
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get('PORT','10000')))
