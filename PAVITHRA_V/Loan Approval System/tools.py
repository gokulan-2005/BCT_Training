from crewai.tools import tool
import sqlite3
import statistics

@tool("Credit Score Service")
def get_credit_score(user_id: str) -> int:
    """
    Compute credit score based on income and loan exposure.
    """

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT monthly_income FROM customers WHERE user_id=?", (user_id,))
    income = cursor.fetchone()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM loans
        WHERE user_id=? AND status='ACTIVE'
    """, (user_id,))
    debt = cursor.fetchone()[0]

    conn.close()

    if not income:
        return 500

    income = income[0]

    ratio = debt / income if income else 1

    if ratio < 0.5:
        return 780
    elif ratio < 1:
        return 700
    else:
        return 620

@tool("Fraud Detection Service")
def check_fraud(user_id: str) -> str:
    """
    Detect anomalies using transaction patterns.
    """

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT amount FROM transactions WHERE user_id=?", (user_id,))
    amounts = [row[0] for row in cursor.fetchall()]
    conn.close()

    if len(amounts) < 2:
        return "LOW_RISK"

    avg = statistics.mean(amounts)
    max_txn = max(amounts)

    if max_txn > avg * 3:
        return "HIGH_RISK"
    elif max_txn > avg * 1.5:
        return "MEDIUM_RISK"

    return "LOW_RISK"

@tool("Loan History Service")
def check_loans(user_id: str) -> dict:
    """
    Fetch active loans and total outstanding.
    """

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), COALESCE(SUM(amount), 0)
        FROM loans
        WHERE user_id=? AND status='ACTIVE'
    """, (user_id,))

    count, total = cursor.fetchone()
    conn.close()

    return {
        "active_loans": count,
        "total_outstanding": total
    }
    
@tool("Income Service")
def get_income(user_id: str) -> float:
    """
    Fetch monthly income.
    """

    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT monthly_income FROM customers WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0
