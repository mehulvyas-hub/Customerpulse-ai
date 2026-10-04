import streamlit as st

# ============================================================
# CUSTOMERPULSE AI
# Snowflake + Streamlit + Cortex AI
# Model: llama3.1-8b
# ============================================================

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="CustomerPulse AI",
    page_icon="🧭",
    layout="wide"
)

# ------------------------------------------------------------
# SNOWFLAKE SESSION
# ------------------------------------------------------------

# Works with Snowflake warehouse-runtime Streamlit.
# The fallback supports container-runtime Streamlit.

try:
    from snowflake.snowpark.context import get_active_session

    session = get_active_session()

except Exception:
    conn = st.connection("snowflake")
    session = conn.session()


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

DATABASE_SCHEMA = "CUSTOMERPULSE_DB.APP"

MODEL = "llama3.1-8b"


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def sql_escape(value):
    """
    Safely escape text before inserting it into a SQL string.
    """
    if value is None:
        return ""

    return str(value).replace("'", "''")


@st.cache_data(ttl=60)
def get_customers():

    query = f"""
        SELECT
            CUSTOMER_ID,
            FULL_NAME
        FROM {DATABASE_SCHEMA}.CUSTOMERS
        ORDER BY FULL_NAME
    """

    rows = session.sql(query).collect()

    return [
        row.as_dict()
        for row in rows
    ]


def get_customer(customer_id):

    customer_id = sql_escape(customer_id)

    query = f"""
        SELECT *
        FROM {DATABASE_SCHEMA}.CUSTOMER_360_V
        WHERE CUSTOMER_ID = '{customer_id}'
    """

    rows = session.sql(query).collect()

    if not rows:
        return None

    return rows[0].as_dict()


def get_next_best_action(customer_id):

    customer_id = sql_escape(customer_id)

    query = f"""
        SELECT
            ENGAGEMENT_BAND,
            NEXT_BEST_ACTION
        FROM {DATABASE_SCHEMA}.NEXT_BEST_ACTION_V
        WHERE CUSTOMER_ID = '{customer_id}'
    """

    rows = session.sql(query).collect()

    if not rows:
        return None

    return rows[0].as_dict()


def get_complaints(customer_id):

    customer_id = sql_escape(customer_id)

    query = f"""
        SELECT
            CREATED_AT,
            CATEGORY,
            STATUS,
            DESCRIPTION
        FROM {DATABASE_SCHEMA}.COMPLAINTS
        WHERE CUSTOMER_ID = '{customer_id}'
        ORDER BY CREATED_AT DESC
    """

    rows = session.sql(query).collect()

    return [
        row.as_dict()
        for row in rows
    ]


# ------------------------------------------------------------
# BUILD CUSTOMER CONTEXT
# ------------------------------------------------------------

def build_customer_context(customer, action):

    return f"""
CUSTOMER INFORMATION

Customer ID:
{customer.get("CUSTOMER_ID", "Not available")}

Name:
{customer.get("FULL_NAME", "Not available")}

City:
{customer.get("CITY", "Not available")}

Segment:
{customer.get("SEGMENT", "Not available")}

Join Date:
{customer.get("JOIN_DATE", "Not available")}

Total Transactions:
{customer.get("TOTAL_TRANSACTIONS", 0)}

Transactions Last 30 Days:
{customer.get("TRANSACTIONS_LAST_30D", 0)}

Total Spend:
{customer.get("TOTAL_SPEND", 0)}

Complaints Last 60 Days:
{customer.get("COMPLAINTS_LAST_60D", 0)}

Open Complaints:
{customer.get("OPEN_COMPLAINTS", 0)}

Days Past Due:
{customer.get("DAYS_PAST_DUE", 0)}

Payment Status:
{customer.get("PAYMENT_STATUS", "Not available")}

Last Call Date:
{customer.get("LAST_CALL_DATE", "Not available")}

Last Call Sentiment:
{customer.get("LAST_CALL_SENTIMENT", "Not available")}

Latest Call Transcript:
{customer.get("LAST_CALL_TRANSCRIPT", "Not available")}

SYSTEM-GENERATED NEXT BEST ACTION

Engagement Band:
{action.get("ENGAGEMENT_BAND", "Not available") if action else "Not available"}

Recommended Action:
{action.get("NEXT_BEST_ACTION", "Not available") if action else "Not available"}
"""


# ------------------------------------------------------------
# AI SUMMARY
# ------------------------------------------------------------

def generate_ai_summary(customer, action):

    context = build_customer_context(
        customer,
        action
    )

    prompt = f"""
You are CustomerPulse AI, an enterprise
customer intelligence copilot.

Use ONLY the customer information supplied below.

DO NOT:
- invent facts
- invent transactions
- invent complaints
- invent financial information
- invent customer events
- change the system-generated recommendation

Explain the recommendation using evidence.

{context}

Return exactly these four sections:

1. Executive Summary
Give a concise overview of the customer's current situation.

2. Key Evidence
List the strongest evidence supporting the situation.

3. Recommended Action
Repeat the system-generated next best action.

4. Why This Action Is Appropriate
Explain why the action is appropriate based only on the evidence.

Keep the answer under 180 words.
"""

    safe_prompt = sql_escape(prompt)

    query = f"""
        SELECT AI_COMPLETE(
            '{MODEL}',
            '{safe_prompt}'
        ) AS ANSWER
    """

    result = session.sql(query).collect()

    if not result:
        return "No AI response was returned."

    return result[0]["ANSWER"]


# ------------------------------------------------------------
# AI CUSTOM QUESTION
# ------------------------------------------------------------

def ask_customer_ai(customer, action, question):

    context = build_customer_context(
        customer,
        action
    )

    prompt = f"""
You are CustomerPulse AI.

Answer the user's question using ONLY the
customer information supplied below.

Do not invent information.

If the answer cannot be determined from the
provided customer information, say:

"That information is not available in the current customer record."

CUSTOMER CONTEXT
================

{context}

USER QUESTION
=============

{question}

Provide a clear, concise business answer.

If appropriate, mention the evidence
supporting your answer.
"""

    safe_prompt = sql_escape(prompt)

    query = f"""
        SELECT AI_COMPLETE(
            '{MODEL}',
            '{safe_prompt}'
        ) AS ANSWER
    """

    result = session.sql(query).collect()

    if not result:
        return "No AI response was returned."

    return result[0]["ANSWER"]


# ============================================================
# HEADER
# ============================================================

st.title("🧭 CustomerPulse AI")

st.caption(
    "Customer 360 + Evidence-Based Next Best Action Engine"
)

st.divider()


# ============================================================
# LOAD CUSTOMERS
# ============================================================

try:

    customers = get_customers()

except Exception as error:

    st.error(
        "Unable to load customers from Snowflake."
    )

    st.code(str(error))

    st.stop()


if not customers:

    st.warning(
        "No customers were found."
    )

    st.stop()


# ============================================================
# CUSTOMER SELECTOR
# ============================================================

customer_map = {
    customer["FULL_NAME"]:
    customer["CUSTOMER_ID"]

    for customer in customers
}

customer_names = list(
    customer_map.keys()
)

# Prefer Rohan for the main demo.
if "Rohan Verma" in customer_names:

    default_index = customer_names.index(
        "Rohan Verma"
    )

else:

    default_index = 0


selected_name = st.selectbox(
    "Select Customer",
    customer_names,
    index=default_index
)

selected_customer_id = customer_map[
    selected_name
]


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

try:

    customer = get_customer(
        selected_customer_id
    )

    action = get_next_best_action(
        selected_customer_id
    )

    complaints = get_complaints(
        selected_customer_id
    )

except Exception as error:

    st.error(
        "Unable to load customer information."
    )

    st.code(str(error))

    st.stop()


if customer is None:

    st.error(
        "Customer 360 information was not found."
    )

    st.stop()


# ============================================================
# TOP METRICS
# ============================================================

st.subheader("Customer Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Segment",
    str(customer.get("SEGMENT", "N/A"))
)

col2.metric(
    "Transactions / 30d",
    int(
        customer.get(
            "TRANSACTIONS_LAST_30D",
            0
        )
    )
)

col3.metric(
    "Open Complaints",
    int(
        customer.get(
            "OPEN_COMPLAINTS",
            0
        )
    )
)

col4.metric(
    "Days Past Due",
    int(
        customer.get(
            "DAYS_PAST_DUE",
            0
        )
    )
)


st.divider()


# ============================================================
# MAIN LAYOUT
# ============================================================

left_column, right_column = st.columns(
    [1.05, 1]
)


# ============================================================
# LEFT COLUMN
# ============================================================

with left_column:

    # --------------------------------------------------------
    # CUSTOMER 360
    # --------------------------------------------------------

    st.subheader("👤 Customer 360")

    st.write(
        f"**Name:** "
        f"{customer.get('FULL_NAME', 'N/A')}"
    )

    st.write(
        f"**Customer ID:** "
        f"{customer.get('CUSTOMER_ID', 'N/A')}"
    )

    st.write(
        f"**City:** "
        f"{customer.get('CITY', 'N/A')}"
    )

    st.write(
        f"**Segment:** "
        f"{customer.get('SEGMENT', 'N/A')}"
    )

    st.write(
        f"**Join Date:** "
        f"{customer.get('JOIN_DATE', 'N/A')}"
    )

    total_spend = customer.get(
        "TOTAL_SPEND",
        0
    )

    st.write(
        f"**Total Spend:** "
        f"₹{float(total_spend):,.0f}"
    )

    st.write(
        f"**Payment Status:** "
        f"{customer.get('PAYMENT_STATUS', 'N/A')}"
    )


    # --------------------------------------------------------
    # CALL INFORMATION
    # --------------------------------------------------------

    st.subheader("📞 Latest Customer Call")

    transcript = customer.get(
        "LAST_CALL_TRANSCRIPT"
    )

    if transcript:

        st.info(transcript)

    else:

        st.info(
            "No call transcript available."
        )


    sentiment = customer.get(
        "LAST_CALL_SENTIMENT",
        "N/A"
    )

    st.write(
        f"**Sentiment:** {sentiment}"
    )


    # --------------------------------------------------------
    # COMPLAINTS
    # --------------------------------------------------------

    st.subheader("📋 Complaints")

    if complaints:

        st.dataframe(
            complaints,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No complaints found."
        )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right_column:

    # --------------------------------------------------------
    # NEXT BEST ACTION
    # --------------------------------------------------------

    st.subheader("🎯 Next Best Action")

    if action:

        band = action.get(
            "ENGAGEMENT_BAND",
            "N/A"
        )

        next_action = action.get(
            "NEXT_BEST_ACTION",
            "No recommendation available."
        )

        if band == "HIGH ATTENTION":

            st.error(
                f"🔴 {band}"
            )

        elif band == "MEDIUM ATTENTION":

            st.warning(
                f"🟡 {band}"
            )

        else:

            st.success(
                f"🟢 {band}"
            )

        st.write(next_action)

    else:

        st.warning(
            "No Next Best Action was found."
        )


    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    st.subheader("🔎 Evidence")

    st.write(
        "✓ "
        f"{customer.get('DAYS_PAST_DUE', 0)} "
        "days past due"
    )

    st.write(
        "✓ "
        f"{customer.get('OPEN_COMPLAINTS', 0)} "
        "open complaints"
    )

    st.write(
        "✓ Latest call sentiment: "
        f"{customer.get('LAST_CALL_SENTIMENT', 'N/A')}"
    )

    if transcript:

        st.write(
            "✓ Latest interaction available"
        )


    # --------------------------------------------------------
    # AI SUMMARY
    # --------------------------------------------------------

    st.subheader("🤖 AI Customer Intelligence")

    if st.button(
        "Generate Customer Intelligence Summary",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing customer information..."
        ):

            try:

                answer = generate_ai_summary(
                    customer,
                    action
                )

                st.markdown(
                    answer
                )

            except Exception as error:

                st.error(
                    "AI summary failed."
                )

                st.code(
                    str(error)
                )


# ============================================================
# ASK CUSTOMERPULSE AI
# ============================================================

st.divider()

st.subheader("💬 Ask CustomerPulse AI")

st.caption(
    "Ask a question about the currently selected customer."
)


question = st.text_input(
    "Your question",
    placeholder=(
        "Example: Why is this customer marked "
        "as high attention?"
    )
)


if st.button(
    "Ask AI",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        with st.spinner(
            "CustomerPulse AI is thinking..."
        ):

            try:

                answer = ask_customer_ai(
                    customer,
                    action,
                    question
                )

                st.markdown("### AI Answer")

                st.markdown(
                    answer
                )

            except Exception as error:

                st.error(
                    "AI question failed."
                )

                st.code(
                    str(error)
                )


# ============================================================
# DEMO QUESTIONS
# ============================================================

st.subheader("💡 Try These Questions")

st.write(
    "• Why is this customer marked as high attention?"
)

st.write(
    "• What evidence supports the recommendation?"
)

st.write(
    "• Why should we contact this customer before upselling?"
)

st.write(
    "• What should the relationship manager resolve first?"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CustomerPulse AI • Snowflake Cortex • "
    "Synthetic demonstration data"
)