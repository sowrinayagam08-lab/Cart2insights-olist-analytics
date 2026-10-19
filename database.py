"""
database.py
-----------
Handles the connection to the MySQL database and runs SQL queries.
Every other file calls run_query() and never touches the connection directly.
"""

import os
from urllib.parse import quote_plus

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# ---- Connection settings (edit these or set them as environment variables) ----
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Arul@nitha08")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "olist_db")  


@st.cache_resource
def get_engine():
    """Create the SQLAlchemy engine once and reuse it across reruns."""
    url = (
        f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame (cached for 10 min)."""
    with get_engine().connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)


def test_connection() -> bool:
    """Return True if the database is reachable."""
    try:
        run_query("SELECT 1")
        return True
    except Exception as exc:
        st.error(f"Database connection failed: {exc}")
        return False
