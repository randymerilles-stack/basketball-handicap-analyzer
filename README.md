# Handicap Multi Cloud v1.5
Deploy-ready Flask diagnostic prototype. **Not** an automatic odds feed or a betting model.

## Deploy on Render
1. Create a GitHub repository and upload these files at repository root.
2. In Render, choose New > Web Service, connect the repository.
3. Choose Python, Free (if offered); build: `pip install -r requirements.txt`; start: `gunicorn app:app`.
4. Open the HTTPS URL Render assigns. `/health` checks service; `/api/status` checks public page reachability.

Public HTML access does not establish permission or an authorised structured odds API. This service does not scrape private endpoints, authenticate to 1xBet, or provide actual handicap markets. Free hosting can sleep or have quotas. Do not enter betting credentials into this prototype.
