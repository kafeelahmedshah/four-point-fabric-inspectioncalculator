import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Four-Point Fabric Inspection Calculator",
    page_icon="🧵",
    layout="wide"
)

st.title("🧵 Four-Point Fabric Inspection Calculator")
st.caption("AI234 Capstone Project | Textile Engineering | Roll No. 25TE051")

st.write(
    "Enter fabric roll dimensions and defect lengths to calculate inspection points "
    "per 100 square yards and classify the inspected roll as Pass or Reject."
)

st.subheader("1. Fabric roll details")
c1, c2, c3 = st.columns(3)
with c1:
    roll_width = st.number_input("Fabric width (inches)", min_value=1.0, value=60.0, step=1.0)
with c2:
    inspected_length = st.number_input("Inspected roll length (yards)", min_value=0.1, value=100.0, step=1.0)
with c3:
    acceptance_limit = st.number_input(
        "Maximum allowed points per 100 sq. yards",
        min_value=0.1, value=40.0, step=1.0,
        help="40 points/100 sq. yd is a commonly used example limit. Confirm the buyer or mill specification."
    )

st.subheader("2. Enter fabric defects")
st.caption(
    "Enter the length of each defect in inches and how many defects have that length. "
    "Add or remove rows using the table controls."
)
default_data = pd.DataFrame({
    "Defect length (inches)": [2.0, 4.0, 7.0, 10.0],
    "Quantity": [2, 1, 1, 0]
})
defects = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Defect length (inches)": st.column_config.NumberColumn(
            "Defect length (inches)", min_value=0.0, step=0.5, format="%.2f"
        ),
        "Quantity": st.column_config.NumberColumn(
            "Quantity", min_value=0, step=1, format="%d"
        )
    },
    key="defect_table"
)

def penalty_for_length(length):
    if length <= 0:
        return 0
    if length <= 3:
        return 1
    if length <= 6:
        return 2
    if length <= 9:
        return 3
    return 4

# Validate and calculate
clean_rows = []
total_defects = 0
total_points = 0
for _, row in defects.iterrows():
    length = float(row["Defect length (inches)"] or 0)
    qty = int(row["Quantity"] or 0)
    if length < 0 or qty < 0:
        st.error("Defect lengths and quantities cannot be negative.")
        st.stop()
    penalty = penalty_for_length(length)
    points = penalty * qty
    total_defects += qty if length > 0 else 0
    total_points += points
    clean_rows.append({
        "Defect length (inches)": length,
        "Quantity": qty,
        "Points per defect": penalty,
        "Total penalty points": points
    })

area_sq_yards = (roll_width / 36.0) * inspected_length
points_per_100 = (total_points / area_sq_yards) * 100 if area_sq_yards > 0 else 0
status = "PASS" if points_per_100 <= acceptance_limit else "REJECT"

st.subheader("3. Inspection result")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total defects", f"{total_defects}")
m2.metric("Total penalty points", f"{total_points}")
m3.metric("Inspected area", f"{area_sq_yards:,.2f} sq. yd")
m4.metric("Points / 100 sq. yd", f"{points_per_100:,.2f}")

if status == "PASS":
    st.success(f"Result: {status} — {points_per_100:.2f} points per 100 sq. yd is within the selected limit of {acceptance_limit:.2f}.")
else:
    st.error(f"Result: {status} — {points_per_100:.2f} points per 100 sq. yd exceeds the selected limit of {acceptance_limit:.2f}.")

st.subheader("4. Defect penalty breakdown")
breakdown = pd.DataFrame(clean_rows)
st.dataframe(breakdown, use_container_width=True, hide_index=True)

if not breakdown.empty:
    chart_data = breakdown.groupby("Points per defect", as_index=False)["Total penalty points"].sum()
    chart_data = chart_data[chart_data["Total penalty points"] > 0]
    if not chart_data.empty:
        fig, ax = plt.subplots()
        ax.bar(chart_data["Points per defect"].astype(str), chart_data["Total penalty points"])
        ax.set_xlabel("Penalty points assigned to each defect")
        ax.set_ylabel("Total penalty points")
        ax.set_title("Inspection penalty-point distribution")
        st.pyplot(fig, clear_figure=True)

st.subheader("5. Four-point grading rule")
rules = pd.DataFrame({
    "Defect length": ["0 to 3 inches", "Over 3 to 6 inches", "Over 6 to 9 inches", "Over 9 inches"],
    "Penalty per defect": [1, 2, 3, 4]
})
st.dataframe(rules, use_container_width=True, hide_index=True)
st.latex(r"\text{Points per 100 sq. yd} = "
         r"\frac{\text{Total penalty points} \times 100}{\text{Inspected area (sq. yd)}}")
st.latex(r"\text{Inspected area (sq. yd)} = "
         r"\frac{\text{Fabric width (inches)}}{36} "
         r"\times \text{Inspected length (yards)}")

with st.expander("Worked example"):
    st.write(
        "For a 60-inch-wide roll with 100 yards inspected, the area is "
        "166.67 square yards. With the default sample defects (2 defects at 2 in, "
        "1 defect at 4 in, and 1 defect at 7 in), the total penalty is 7 points. "
        "The inspection score is 4.20 points per 100 square yards."
    )

st.subheader("Limitations & Responsible Use")
st.write("""
- This is an educational calculator based on a simplified four-point defect-length schedule.
- The acceptance limit is editable; 40 points per 100 square yards is shown as a commonly used example, not a universal buyer requirement.
- Confirm the applicable inspection standard, buyer specification, defect definitions, and sampling plan before using results for commercial acceptance.
- This calculator does not use a trained AI or computer-vision model; the result is calculated from the defect lengths and quantities entered by the user.
- Accurate inspection depends on correct defect identification, measurement, fabric width, and inspected length.
- No personal data is collected or stored by this application.
""")

st.caption("AI234 Individual Capstone Project | Roll No. 25TE051")
