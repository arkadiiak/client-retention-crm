-- Analytical queries for the client retention CRM
-- Demonstrates: CASE segmentation, aggregation, joins, subqueries

-- 1. Segment clients by visit frequency, with count and avg spend per segment
SELECT
    CASE
        WHEN visits >= 40 THEN 'High Value (40+)'
        WHEN visits >= 20 THEN 'Mid Value (20-39)'
        WHEN visits >= 10 THEN 'Regular (10-19)'
        ELSE 'New / Light (0-9)'
    END AS segment,
    COUNT(*) AS client_count,
    ROUND(AVG(spend_gbp), 2) AS avg_spend,
    ROUND(SUM(spend_gbp), 2) AS total_spend
FROM client_database
GROUP BY segment
ORDER BY avg_spend DESC;

-- 2. Contact result breakdown, with % of total
SELECT
    contact_result,
    COUNT(*) AS client_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM client_database), 1) AS pct_of_total
FROM client_database
GROUP BY contact_result
ORDER BY client_count DESC;

-- 3. Top 10 highest-value clients still showing 'No Response'
SELECT client_id, spend_gbp, visits, last_visit
FROM client_database
WHERE contact_result = 'No Response'
ORDER BY spend_gbp DESC
LIMIT 10;

-- 4. Recovery outcomes by outreach method (from action log)
SELECT
    method,
    COUNT(*) AS attempts,
    SUM(CASE WHEN result LIKE 'Booked%' THEN 1 ELSE 0 END) AS booked_outcomes,
    ROUND(100.0 * SUM(CASE WHEN result LIKE 'Booked%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_rate_pct
FROM recovery_action_log
GROUP BY method
ORDER BY success_rate_pct DESC;

-- 5. Clients with an open follow-up (has a follow-up date, not yet resolved)
SELECT c.client_id, c.spend_gbp, a.contact_date, a.followup_date, a.notes
FROM recovery_action_log a
JOIN client_database c ON c.client_id = a.client_id
WHERE a.followup_date IS NOT NULL
ORDER BY a.followup_date ASC;
