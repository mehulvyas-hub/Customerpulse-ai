
# CustomerPulse AI

Solo-hackathon MVP for the Snowflake CoCo CLI Hackathon – GCC Edition.

## Demo flow

1. Search/select a customer.
2. Show Customer 360 from structured Snowflake tables.
3. Show the latest call transcript and AI sentiment.
4. Show a deterministic, auditable Next Best Action.
5. Ask the AI copilot to explain the customer situation using only the displayed facts.
6. Show evidence and avoid unsupported claims.

## Snowflake objects

- CUSTOMERPULSE_DB.APP.CUSTOMERS
- CUSTOMERPULSE_DB.APP.LOANS
- CUSTOMERPULSE_DB.APP.TRANSACTIONS
- CUSTOMERPULSE_DB.APP.COMPLAINTS
- CUSTOMERPULSE_DB.APP.CALL_TRANSCRIPTS
- CUSTOMERPULSE_DB.APP.CALL_ANALYSIS
- CUSTOMERPULSE_DB.APP.CUSTOMER_360_V
- CUSTOMERPULSE_DB.APP.NEXT_BEST_ACTION_V

## Suggested demo customer

Use C1003 (Rohan Verma). He has overdue loan days, two open complaints, and a negative service call.

## Deploy

Create a Streamlit app in Snowflake:
Projects -> Streamlit -> + Streamlit App.
Copy `app/streamlit_app.py` into the app editor, choose database/schema and an X-SMALL warehouse, then run.

Do not commit account passwords, private keys, tokens, or connection files.
