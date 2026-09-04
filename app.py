import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Ferry Analytics Dashboard",
    page_icon="⛴️",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

analysis_df = pd.read_csv("ferry_analysis_data.csv")

analysis_df["Timestamp"] = pd.to_datetime(
    analysis_df["Timestamp"]
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

years = sorted(
    analysis_df["Year"].dropna().unique()
)

seasons = sorted(
    analysis_df["Season"].dropna().unique()
)

day_types = sorted(
    analysis_df["DayType"].dropna().unique()
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All Years"] + years
)

selected_season = st.sidebar.selectbox(
    "Select Season",
    ["All Seasons"] + seasons
)

selected_day_type = st.sidebar.selectbox(
    "Select Day Type",
    ["All Days"] + day_types
)

# --------------------------------------------------
# DATE RANGE FILTER
# --------------------------------------------------

min_date = analysis_df["Timestamp"].min().date()
max_date = analysis_df["Timestamp"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# --------------------------------------------------
# RESET FILTERS
# --------------------------------------------------

if st.sidebar.button("Reset Filters"):
    st.rerun()

# --------------------------------------------------
# ABOUT & METHODOLOGY
# --------------------------------------------------

with st.sidebar.expander("ℹ️ About This Dashboard"):

    st.markdown(
        """
        ### Project Overview

        This dashboard analyzes ferry capacity utilization
        and operational efficiency using historical activity data.

        ### Key Metrics

        **Total Activity Load**  
        Combined operational activity based on sales
        and redemption counts.

        **OLI**  
        Operational Load Indicator used to measure
        activity pressure.

        **Congestion Rate**  
        Percentage of observed periods identified
        as congested.

        **Idle Rate**  
        Percentage of observed periods showing
        idle capacity.

        **Peak Strain**  
        Maximum continuous operational strain
        identified during the analysis.

        ### Filters

        Use the sidebar filters to analyze operations
        by:

        - Year
        - Season
        - Day Type

        All charts and insights update according
        to the selected filters.
        """
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = analysis_df.copy()

if selected_year != "All Years":
    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]

if selected_season != "All Seasons":
    filtered_df = filtered_df[
        filtered_df["Season"] == selected_season
    ]

if selected_day_type != "All Days":
    filtered_df = filtered_df[
        filtered_df["DayType"] == selected_day_type
    ]



# --------------------------------------------------
# DAY NAMES
# --------------------------------------------------

day_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics System"
)

st.markdown(
    """
    This dashboard analyzes ferry activity patterns, capacity utilization,
    congestion, and idle-capacity periods to identify operational
    inefficiencies and high-demand time windows.
    """
)

st.info(
    "Use the filters in the sidebar to explore ferry operations by year, season, and day type."
)


# --------------------------------------------------
# TABS
# --------------------------------------------------

overview_tab, activity_tab, operations_tab, data_tab = st.tabs(
    [
        "🏠 Overview",
        "📊 Activity Analysis",
        "🚦 Operations",
        "📋 Data & Recommendations"
    ]
)


# ==================================================
# OVERVIEW TAB
# ==================================================

with overview_tab:

    st.header("Executive Overview")

    if not filtered_df.empty:

        # --------------------------------------------------
        # KPI CALCULATIONS
        # --------------------------------------------------

        avg_activity = (
            filtered_df["Total Activity Load"].mean()
        )

        congestion_rate = (
            filtered_df["Congestion"].mean() * 100
        )

        idle_rate = (
            filtered_df["Idle Capacity"].mean() * 100
        )

        peak_strain = 585

        hour_activity = (
            filtered_df
            .groupby("Hour")["Total Activity Load"]
            .mean()
        )

        busiest_hour = hour_activity.idxmax()

        season_activity = (
            filtered_df
            .groupby("Season")["Total Activity Load"]
            .mean()
        )

        busiest_season = season_activity.idxmax()

        day_activity = (
            filtered_df
            .groupby("DayType")["Total Activity Load"]
            .mean()
        )

        busiest_day = day_activity.idxmax()


        # --------------------------------------------------
        # KPI ROW 1
        # --------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average Activity",
                f"{avg_activity:.2f}"
            )

        with col2:
            st.metric(
                "Congestion Rate",
                f"{congestion_rate:.2f}%"
            )

        with col3:
            st.metric(
                "Idle Rate",
                f"{idle_rate:.2f}%"
            )

        with col4:
            st.metric(
                "Peak Strain",
                f"{peak_strain} min"
            )


        # --------------------------------------------------
        # KPI ROW 2
        # --------------------------------------------------

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            st.metric(
                "Busiest Hour",
                f"{busiest_hour}:00"
            )

        with col6:
            st.metric(
                "Busiest Season",
                busiest_season
            )

        with col7:
            st.metric(
                "Busiest Day Type",
                busiest_day
            )

        with col8:
            st.metric(
                "Records Analyzed",
                f"{len(filtered_df):,}"
            )


        st.divider()


        # --------------------------------------------------
        # EXECUTIVE INSIGHTS
        # --------------------------------------------------

        st.subheader("Executive Insights")

        busiest_hour_value = (
            hour_activity.max()
        )

        highest_congestion_hour = (
            filtered_df
            .groupby("Hour")["Congestion"]
            .mean()
            .idxmax()
        )

        highest_idle_hour = (
            filtered_df
            .groupby("Hour")["Idle Capacity"]
            .mean()
            .idxmax()
        )


        insight_col1, insight_col2 = st.columns(2)

        with insight_col1:

            st.info(
                f"🚦 **Peak Activity Window:** "
                f"{busiest_hour}:00 shows the highest "
                f"average activity load "
                f"({busiest_hour_value:.2f})."
            )

            st.warning(
                f"⚠️ **Highest Congestion Hour:** "
                f"{highest_congestion_hour}:00."
            )


        with insight_col2:

            st.info(
                f"💤 **Highest Idle Hour:** "
                f"{highest_idle_hour}:00."
            )

            st.success(
                f"📊 **Records Analyzed:** "
                f"{len(filtered_df):,}"
            )


        st.divider()


        # --------------------------------------------------
        # QUICK ACTIVITY CHART
        # --------------------------------------------------

        st.subheader("Average Activity by Year")

        yearly_activity = (
            filtered_df
            .groupby("Year")["Total Activity Load"]
            .mean()
            .reset_index()
        )

        fig_year = px.line(
            yearly_activity,
            x="Year",
            y="Total Activity Load",
            markers=True,
            title="Average Ferry Activity by Year"
        )

        fig_year.update_layout(
            xaxis_title="Year",
            yaxis_title="Average Activity Load",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_year,
            use_container_width=True
        )

    else:

        st.warning(
            "No records match the selected filters."
        )


# ==================================================
# ACTIVITY ANALYSIS TAB
# ==================================================

with activity_tab:

    st.header("Activity Analysis")

    if not filtered_df.empty:

        # --------------------------------------------------
        # ACTIVITY BY HOUR
        # --------------------------------------------------

        st.subheader("Average Activity by Hour")

        hourly_activity = (
            filtered_df
            .groupby("Hour")["Total Activity Load"]
            .mean()
            .reset_index()
        )

        fig_hour = px.bar(
            hourly_activity,
            x="Hour",
            y="Total Activity Load",
            title="Average Ferry Activity by Hour"
        )

        fig_hour.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Average Activity Load"
        )

        st.plotly_chart(
            fig_hour,
            use_container_width=True
        )


        # --------------------------------------------------
        # SEASON
        # --------------------------------------------------

        st.subheader("Average Activity by Season")

        seasonal_activity = (
            filtered_df
            .groupby("Season")["Total Activity Load"]
            .mean()
            .reset_index()
        )

        fig_season = px.bar(
            seasonal_activity,
            x="Season",
            y="Total Activity Load",
            title="Average Ferry Activity by Season"
        )

        fig_season.update_layout(
            xaxis_title="Season",
            yaxis_title="Average Activity Load"
        )

        st.plotly_chart(
            fig_season,
            use_container_width=True
        )


        # --------------------------------------------------
        # DAY TYPE
        # --------------------------------------------------

        st.subheader("Average Activity: Weekday vs Weekend")

        daytype_activity = (
            filtered_df
            .groupby("DayType")["Total Activity Load"]
            .mean()
            .reset_index()
        )

        fig_daytype = px.bar(
            daytype_activity,
            x="DayType",
            y="Total Activity Load",
            title="Average Activity: Weekday vs Weekend"
        )

        fig_daytype.update_layout(
            xaxis_title="Day Type",
            yaxis_title="Average Activity Load"
        )

        st.plotly_chart(
            fig_daytype,
            use_container_width=True
        )


        # --------------------------------------------------
        # DAY OF WEEK
        # --------------------------------------------------

        st.subheader("Average Activity by Day of Week")

        day_activity_chart = (
            filtered_df
            .groupby("DayOfWeek")["Total Activity Load"]
            .mean()
            .reset_index()
        )

        day_activity_chart["Day"] = (
            day_activity_chart["DayOfWeek"]
            .map(day_names)
        )

        day_activity_chart["Day"] = pd.Categorical(
            day_activity_chart["Day"],
            categories=day_order,
            ordered=True
        )

        day_activity_chart = (
            day_activity_chart
            .sort_values("Day")
        )

        fig_day = px.bar(
            day_activity_chart,
            x="Day",
            y="Total Activity Load",
            title="Average Ferry Activity by Day of Week"
        )

        fig_day.update_layout(
            xaxis_title="Day of Week",
            yaxis_title="Average Activity Load"
        )

        st.plotly_chart(
            fig_day,
            use_container_width=True
        )


        # --------------------------------------------------
        # HEATMAP
        # --------------------------------------------------

        st.subheader(
            "Activity Heatmap: Day of Week vs Hour"
        )

        heatmap_data = (
            filtered_df
            .groupby(
                ["DayOfWeek", "Hour"]
            )["Total Activity Load"]
            .mean()
            .reset_index()
        )

        heatmap_data["Day"] = (
            heatmap_data["DayOfWeek"]
            .map(day_names)
        )

        heatmap_data["Day"] = pd.Categorical(
            heatmap_data["Day"],
            categories=day_order,
            ordered=True
        )

        heatmap_data = heatmap_data.sort_values(
            ["Day", "Hour"]
        )

        fig_heatmap = px.density_heatmap(
            heatmap_data,
            x="Hour",
            y="Day",
            z="Total Activity Load",
            category_orders={
                "Day": day_order
            },
            title="Average Activity by Day and Hour",
            text_auto=".0f"
        )

        fig_heatmap.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )

    else:

        st.warning(
            "No activity data available for the selected filters."
        )


# ==================================================
# OPERATIONS TAB
# ==================================================

with operations_tab:

    st.header("Operational Analysis")

    if not filtered_df.empty:

        # --------------------------------------------------
        # CONGESTION VS IDLE
        # --------------------------------------------------

        st.subheader(
            "Congestion vs Idle Rate by Hour"
        )

        hourly_operational = (
            filtered_df
            .groupby("Hour")[
                ["Congestion", "Idle Capacity"]
            ]
            .mean()
            .reset_index()
        )

        hourly_operational["Congestion Rate"] = (
            hourly_operational["Congestion"] * 100
        )

        hourly_operational["Idle Rate"] = (
            hourly_operational["Idle Capacity"] * 100
        )

        operational_long = hourly_operational.melt(
            id_vars="Hour",
            value_vars=[
                "Congestion Rate",
                "Idle Rate"
            ],
            var_name="Metric",
            value_name="Rate"
        )

        fig_operational = px.line(
            operational_long,
            x="Hour",
            y="Rate",
            color="Metric",
            markers=True,
            title="Congestion vs Idle Rate by Hour"
        )

        fig_operational.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Rate (%)",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_operational,
            use_container_width=True
        )


        # --------------------------------------------------
        # CONGESTION HOTSPOTS
        # --------------------------------------------------

        st.subheader("Top Congestion Hotspots")

        congestion_hotspots = (
            filtered_df[
                filtered_df["Congestion"]
            ]
            .groupby(
                ["DayOfWeek", "Hour"]
            )
            .size()
            .reset_index(
                name="Congestion Intervals"
            )
        )

        congestion_hotspots["Day"] = (
            congestion_hotspots["DayOfWeek"]
            .map(day_names)
        )

        congestion_hotspots = (
            congestion_hotspots
            .sort_values(
                "Congestion Intervals",
                ascending=False
            )
            .head(10)
        )

        congestion_hotspots["Day & Hour"] = (
            congestion_hotspots["Day"]
            + " - "
            + congestion_hotspots["Hour"].astype(str)
            + ":00"
        )

        st.dataframe(
            congestion_hotspots[
                [
                    "Day & Hour",
                    "Congestion Intervals"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


        # --------------------------------------------------
        # IDLE HOTSPOTS
        # --------------------------------------------------

        st.subheader(
            "Top Idle-Capacity Hotspots"
        )

        idle_hotspots = (
            filtered_df[
                filtered_df["Idle Capacity"]
            ]
            .groupby(
                ["DayOfWeek", "Hour"]
            )
            .size()
            .reset_index(
                name="Idle Intervals"
            )
        )

        idle_hotspots["Day"] = (
            idle_hotspots["DayOfWeek"]
            .map(day_names)
        )

        idle_hotspots = (
            idle_hotspots
            .sort_values(
                "Idle Intervals",
                ascending=False
            )
            .head(10)
        )

        idle_hotspots["Day & Hour"] = (
            idle_hotspots["Day"]
            + " - "
            + idle_hotspots["Hour"].astype(str)
            + ":00"
        )

        st.dataframe(
            idle_hotspots[
                [
                    "Day & Hour",
                    "Idle Intervals"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


        # --------------------------------------------------
        # OPERATIONAL RECOMMENDATIONS
        # --------------------------------------------------

        st.subheader(
            "Operational Recommendations"
        )

        avg_congestion = (
            filtered_df["Congestion"].mean() * 100
        )

        avg_idle = (
            filtered_df["Idle Capacity"].mean() * 100
        )

        busiest_hour = (
            filtered_df
            .groupby("Hour")["Total Activity Load"]
            .mean()
            .idxmax()
        )

        highest_congestion_hour = (
            filtered_df
            .groupby("Hour")["Congestion"]
            .mean()
            .idxmax()
        )

        highest_idle_hour = (
            filtered_df
            .groupby("Hour")["Idle Capacity"]
            .mean()
            .idxmax()
        )


        if avg_congestion > 5:

            st.warning(
                f"🚦 Consider increasing operational capacity "
                f"around {highest_congestion_hour}:00, "
                f"where congestion is highest."
            )

        else:

            st.success(
                "✅ Overall congestion is relatively controlled."
            )


        if avg_idle > 5:

            st.info(
                f"💤 Review scheduling and resource allocation "
                f"around {highest_idle_hour}:00 to reduce "
                f"idle capacity."
            )

        else:

            st.success(
                "✅ Idle capacity is relatively controlled."
            )


        st.info(
            f"📈 Prioritize capacity planning around "
            f"{busiest_hour}:00, the highest activity period."
        )

    else:

        st.warning(
            "No operational data available for the selected filters."
        )


# ==================================================
# DATA & RECOMMENDATIONS TAB
# ==================================================

with data_tab:

    st.header("Data & Detailed Analysis")
    if not filtered_df.empty:

        # --------------------------------------------------
        # DATASET SUMMARY
        # --------------------------------------------------

        st.subheader("Dataset Summary")

        summary_col1, summary_col2, summary_col3, summary_col4 = (
            st.columns(4)
        )

        with summary_col1:

            st.metric(
                "Total Records",
                f"{len(filtered_df):,}"
            )

        with summary_col2:

            start_date = filtered_df["Timestamp"].min()

            st.metric(
                "Start Date",
                start_date.strftime("%d %b %Y")
            )

        with summary_col3:

            end_date = filtered_df["Timestamp"].max()

            st.metric(
                "End Date",
                end_date.strftime("%d %b %Y")
            )

        with summary_col4:

            st.metric(
                "Columns",
                len(filtered_df.columns)
            )


        st.divider()

        

        # --------------------------------------------------
        # TOP ACTIVITY PERIODS
        # --------------------------------------------------

        st.subheader(
            "Top 10 Highest-Activity Periods"
        )

        top_activity = (
            filtered_df[
                [
                    "Timestamp",
                    "Sales Count",
                    "Redemption Count",
                    "Total Activity Load",
                    "OLI"
                ]
            ]
            .sort_values(
                "Total Activity Load",
                ascending=False
            )
            .head(10)
            .copy()
        )

        top_activity["Timestamp"] = (
            top_activity["Timestamp"]
            .dt.strftime("%d %b %Y, %H:%M")
        )

        st.dataframe(
            top_activity,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


# --------------------------------------------------
# FILTERED DATA
# --------------------------------------------------

with st.expander("View Filtered Data"):

    st.write(
        f"Showing {len(filtered_df):,} records "
        "based on the selected filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # Download filtered dataset
    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv_data,
        file_name="filtered_ferry_data.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Ferry Capacity Utilization & Operational Efficiency Analytics System "
    " | Data Analytics Project"
)