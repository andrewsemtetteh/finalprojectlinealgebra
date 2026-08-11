import streamlit as st

from main import analyzePlaneIntersection, createPlaneVisual


st.set_page_config(
    page_title="Plane Intersection",
    page_icon="📐",
    layout="wide",
)

st.title("Finding the Intersection Line of Two Planes in 3D Space")
st.markdown(
    "Enter the coefficients for two planes in the form **ax + by + cz = d**. "
    "The app computes the intersection line when it exists and visualizes both planes."
)

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Plane A")
    a1 = st.number_input("a₁", value=1.0, key="a1")
    b1 = st.number_input("b₁", value=1.0, key="b1")
    c1 = st.number_input("c₁", value=1.0, key="c1")
    d1 = st.number_input("d₁", value=6.0, key="d1")

with col_b:
    st.subheader("Plane B")
    a2 = st.number_input("a₂", value=1.0, key="a2")
    b2 = st.number_input("b₂", value=-1.0, key="b2")
    c2 = st.number_input("c₂", value=2.0, key="c2")
    d2 = st.number_input("d₂", value=2.0, key="d2")

plane_a = [a1, b1, c1, d1]
plane_b = [a2, b2, c2, d2]

st.markdown("### Plane Equations")
st.latex(f"{a1:g}x + {b1:g}y + {c1:g}z = {d1:g}")
st.latex(f"{a2:g}x + {b2:g}y + {c2:g}z = {d2:g}")

analysis = analyzePlaneIntersection(plane_a, plane_b)

st.markdown("### Result")
if analysis["case"] == "line":
    st.success(analysis["explanation"])
elif analysis["case"] == "parallel":
    st.warning(analysis["explanation"])
elif analysis["case"] == "coincident":
    st.info(analysis["explanation"])

with st.expander("Show step-by-step RREF calculation"):
    for step in analysis["steps"]:
        st.text(step)
        st.divider()

fig, _ = createPlaneVisual(plane_a, plane_b)
st.plotly_chart(fig, use_container_width=True)
