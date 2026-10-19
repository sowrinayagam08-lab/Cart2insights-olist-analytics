"""
utils.py  (v2)
--------------
Reusable helpers: formatting, chart builders, Brazil bubble map,
empty-data guard, and the Observation -> Interpretation -> Business Impact box.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

CURRENCY = "R$"  # Olist prices are in Brazilian Reais

# Approximate centre point of each Brazilian state (for the bubble map)
STATE_COORDS = {
    "AC": (-9.02, -70.81), "AL": (-9.57, -36.78), "AM": (-3.47, -65.10),
    "AP": (1.41, -51.77),  "BA": (-12.96, -41.70), "CE": (-5.20, -39.53),
    "DF": (-15.83, -47.86), "ES": (-19.19, -40.34), "GO": (-15.83, -49.84),
    "MA": (-5.42, -45.44), "MG": (-18.10, -44.38), "MS": (-20.51, -54.54),
    "MT": (-12.64, -55.42), "PA": (-3.79, -52.48), "PB": (-7.28, -36.72),
    "PE": (-8.38, -37.86), "PI": (-6.60, -42.28), "PR": (-24.89, -51.55),
    "RJ": (-22.25, -42.66), "RN": (-5.81, -36.59), "RO": (-10.83, -63.34),
    "RR": (2.74, -62.08),  "RS": (-30.17, -53.50), "SC": (-27.45, -50.95),
    "SE": (-10.57, -37.45), "SP": (-22.19, -48.79), "TO": (-9.46, -48.26),
}


# ---------- Formatting ----------
def fmt_money(value) -> str:
    """12345678 -> R$ 12.35M"""
    if value is None or pd.isna(value):
        return "-"
    for limit, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
        if abs(value) >= limit:
            return f"{CURRENCY} {value / limit:,.2f}{suffix}"
    return f"{CURRENCY} {value:,.2f}"


def fmt_int(value) -> str:
    return "-" if value is None or pd.isna(value) else f"{int(value):,}"


# ---------- Layout ----------
def section_header(title: str, subtitle: str = ""):
    st.header(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def kpi_row(items: list[tuple[str, str]]):
    """items = [(label, formatted_value), ...] -> one st.metric per column."""
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)


def empty_warning(df: pd.DataFrame) -> bool:
    """Show a message and return True when a query returned nothing."""
    if df is None or df.empty:
        st.warning("No data for the selected filters. Try a different year or state.")
        return True
    return False


def insight_box(observation: str, interpretation: str, impact: str):
    """Step 11: Observation -> Interpretation -> Business Impact."""
    with st.container(border=True):
        st.markdown("**Business Insight**")
        st.markdown(f"**Observation:** {observation}")
        st.markdown(f"**Interpretation:** {interpretation}")
        st.markdown(f"**Business Impact:** {impact}")


# ---------- Charts ----------
def line_chart(df, x, y, title, **kw):
    fig = px.line(df, x=x, y=y, markers=True, title=title, **kw)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig


def bar_chart(df, x, y, title, horizontal=False, color=None, **kw):
    if horizontal:
        fig = px.bar(df, x=y, y=x, orientation="h", title=title, color=color, **kw)
        fig.update_layout(yaxis=dict(autorange="reversed"))
    else:
        fig = px.bar(df, x=x, y=y, title=title, color=color, **kw)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig


def pie_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values, title=title, hole=0.4)
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
    return fig


def state_map(df, state_col, size_col, color_col, title):
    """Bubble map of Brazil: bubble size = size_col, colour = color_col."""
    data = df.copy()
    data["lat"] = data[state_col].map(lambda s: STATE_COORDS.get(s, (None, None))[0])
    data["lon"] = data[state_col].map(lambda s: STATE_COORDS.get(s, (None, None))[1])
    data = data.dropna(subset=["lat", "lon"])
    fig = px.scatter_geo(
        data, lat="lat", lon="lon", size=size_col, color=color_col,
        hover_name=state_col, size_max=45, title=title,
        color_continuous_scale="Turbo",
    )
    fig.update_geos(fitbounds="locations", showcountries=True, showland=True,
                    landcolor="#1A1F2B", countrycolor="#555", bgcolor="rgba(0,0,0,0)")
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0), height=500)
    return fig


def show(fig):
    st.plotly_chart(fig, use_container_width=True)
