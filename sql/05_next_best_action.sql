CREATE OR REPLACE VIEW CUSTOMERPULSE_DB.APP.NEXT_BEST_ACTION_V AS

SELECT

    CUSTOMER_ID,

    CASE

        WHEN DAYS_PAST_DUE >= 15
             AND OPEN_COMPLAINTS >= 1
        THEN
            'Priority relationship-manager callback; resolve the loan/service issue before any upsell.'

        WHEN OPEN_COMPLAINTS >= 2
        THEN
            'Escalate unresolved complaints to priority support and schedule a callback within 24 hours.'

        WHEN LAST_CALL_SENTIMENT = 'negative'
        THEN
            'Proactive service-recovery call focused on the customer complaint before promotional outreach.'

        WHEN TRANSACTIONS_LAST_30D <= 1
             AND SEGMENT = 'Premium'
        THEN
            'Re-engagement outreach based on recent inactivity; avoid an immediate promotional upsell.'

        ELSE
            'Routine relationship review with a personalized offer based on recent customer activity.'

    END AS NEXT_BEST_ACTION,

    CASE

        WHEN DAYS_PAST_DUE >= 15
             OR OPEN_COMPLAINTS >= 2
             OR LAST_CALL_SENTIMENT = 'negative'
        THEN
            'HIGH ATTENTION'

        WHEN DAYS_PAST_DUE >= 3
             OR OPEN_COMPLAINTS = 1
        THEN
            'MEDIUM ATTENTION'

        ELSE
            'STABLE'

    END AS ENGAGEMENT_BAND

FROM CUSTOMERPULSE_DB.APP.CUSTOMER_360_V;

SELECT *
FROM CUSTOMERPULSE_DB.APP.NEXT_BEST_ACTION_V
WHERE CUSTOMER_ID = 'C1003';

SHOW CORTEX BASE MODELS;

SELECT AI_COMPLETE(
    'llama3.1-8b',
    'Explain Customer 360 in one sentence.'
);