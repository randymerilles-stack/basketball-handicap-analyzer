# Handicap Multi Cloud v1.6

Android-friendly Flask dashboard with an automatic 30-second polling interface and a structured feed adapter. **It is not connected to live 1xBet markets by default.** The public 1xBet page is only a reference URL; no unofficial private endpoints or credentials are used.

## Deployment

Replace the five root files in your existing GitHub repository and Render auto-deploys from `main`. Existing Render free service and settings can remain unchanged. No new account required.

## Optional licensed feed

Set the `MARKET_FEED_URL` environment variable on Render to an HTTPS JSON endpoint that you are authorised to access. Endpoint must return:

```json
{"games":[{"id":"unique-match-id","league":"Example League","home":"Team A","away":"Team B","home_score":62,"away_score":58,"period":"Q3","clock":"05:30","handicaps":[{"side":"home","line":-3.5,"odds":1.9},{"side":"away","line":3.5,"odds":1.9}]}]}
```

Only feed-supplied markets are displayed. Rejects invalid selections and games. Polls the configured provider at most once per 30 seconds per server process. The feed should explicitly represent *full-game* handicap including overtime where applicable; do not mix markets.

## Multi policy

Always returns `NO MULTI` until a separate, backtested, calibrated spread-cover probability model is implemented. Break-even implied probabilities (`1/odds`) are **not** predicted win probabilities. No bet execution or account authentication.

## Endpoints

- `/` Dashboard
- `/health` Liveness
- `/api/status` Feed state, validated market data, multi state
