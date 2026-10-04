SELECT

    CUSTOMER_ID,

    FULL_NAME,

    AI_COMPLETE(
        'llama3.1-8b',

        CONCAT(

            'You are CustomerPulse AI, an enterprise '
            || 'customer intelligence copilot. ',

            'Use ONLY the supplied customer facts. '
            || 'Do not invent customer information. ',

            '\nCustomer: '
            || FULL_NAME,

            '\nSegment: '
            || SEGMENT,

            '\nTransactions last 30 days: '
            || TRANSACTIONS_LAST_30D,

            '\nTotal spend: '
            || TOTAL_SPEND,

            '\nOpen complaints: '
            || OPEN_COMPLAINTS,

            '\nDays past due: '
            || DAYS_PAST_DUE,

            '\nPayment status: '
            || PAYMENT_STATUS,

            '\nLast call sentiment: '
            || LAST_CALL_SENTIMENT,

            '\nLatest call: '
            || LAST_CALL_TRANSCRIPT,

            '\n\nExplain:',

            '\n1. Executive summary',

            '\n2. Key evidence',

            '\n3. Recommended action',

            '\n4. Why this action is appropriate',

            '\nKeep the response under 180 words.'
        )

    ) AS AI_EXPLANATION

FROM CUSTOMERPULSE_DB.APP.CUSTOMER_360_V

WHERE CUSTOMER_ID = 'C1003';