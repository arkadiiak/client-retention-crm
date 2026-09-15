# Client Retention CRM — Lost Client Recovery System

## Overview
A structured database for tracking and recovering lapsed clients at a high-volume beauty salon.
The system identifies clients who have not returned within a set timeframe, segments them by value and visit history, and tracks all outreach attempts and outcomes.

## The Problem This Solves
In a busy service business, clients stop coming back for many reasons — price sensitivity, life changes, or a single bad experience. Without a system, these clients are simply lost. This CRM tracks every lapsed client, every contact attempt, and every outcome — turning passive churn into an active recovery process.

## How It Works (My Process)
- Export lapsed client list from booking system (Zenoti) — filtered by last visit date
- Segment clients by visit count: 20+, 10+, 5+, 0–5
- Prioritise high-value clients (20+ visits, £1,000+ spend) for personal outreach
- Contact via email + WhatsApp — personalised message based on history
- Log result in tracker: No Response / Replied / Booked / Not Lost Client
- Follow up on No Response cases after 7–14 days
- Review weekly — track recovery rate and adjust messaging

## What's Inside (3 Sheets)

### Sheet 1 — High Value Clients (20+ visits)
Top-tier lapsed clients sorted by total spend. Each row includes:
- Anonymised client ID
- Total lifetime spend
- Number of visits
- First and last visit dates
- Contact result (colour-coded)
- Action notes from outreach

### Sheet 2 — Mid-Value Clients (£1,000–£2,000 spend)
Same structure for the mid-value segment — clients with strong history but lower frequency.

### Sheet 3 — Retention Summary Dashboard

| Metric | Value |
|--------|-------|
| Total clients tracked | 130+ |
| No Response | 81 (62%) |
| Not Lost Client confirmed | 25 (19%) |
| Replied | 17 (13%) |
| Booked / Recovered | 8 (6%) |

## Contact Status Key

| Status | Meaning |
|--------|---------|
| 🔴 No Response | Contacted, no reply — requires follow-up |
| 🟡 Replied | Responded but not yet booked |
| 🟢 Booked | Successfully recovered — appointment made |
| 🟣 Not Lost Client | Confirmed still active — removed from lapsed list |

## Skills Demonstrated
- CRM database design and management
- Client segmentation by spend and visit frequency
- Outreach tracking and follow-up management
- Retention rate analysis
- Operational notes and decision logging
- SQL and Python-based client segmentation and recovery analysis

## Tools Used
Google Sheets (operational) → anonymised and rebuilt in Excel for portfolio · SQL (CASE segmentation, joins, subqueries) · Python (pandas, sqlite3, matplotlib)
Booking data sourced from Zenoti salon management system

---

## SQL + Python Implementation
This project also includes SQL (`schema_retention.sql`, `queries_retention.sql`) and Python (`analyze_retention.py`) versions of the CRM logic, using the anonymised client database to demonstrate:
- Client segmentation by visit frequency with spend analysis
- Contact outcome breakdown and high-value unresponsive client flagging
- Recovery success rate analysis by outreach method
- Client-by-segment visualisation
