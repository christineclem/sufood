# Tally-SQL CRM
A lightweight web service that accepts Tally form submissions via webhook and stores them in a PostgreSQL database (Supabase).

## How It Works
Tally form → POST webhook → app.py (Render.com) → Supabase PostgreSQL

## Setup
1. Clone repo
2. pip install -r requirements.txt
3. Set environment variables

## Environment Variables
DATABASE_URL="supabase_direct_connection_string"
Select the direct connection string Session Pooler (IPv4).

## Deployment
Connect repo to Render.com and set app.py as the entry point.

## Endpoints
POST /webhook — receives Tally form submissions

## Roadmap
- Sales tracking - 27 Apr 2026
- Customer anonymisation (GDPR delete) - 28 Apr 2026
- Loyal customer discount labelling (fixed & variable) - 30 Apr 2026
- Tally-independent HTML submission interface - 4 May 2026
