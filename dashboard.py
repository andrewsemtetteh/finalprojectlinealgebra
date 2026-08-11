import streamlit as st

from main import analyzePlaneIntersection, createPlaneVisual


st.set_page_config(
    page_title="Plane Intersection",
    page_icon="📐",
    layout="wide",
)

st.markdown(
    """
    <style>
    .app-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .app-subtitle {
        text-align: center;
        font-size: 1.05rem;
        color: #444;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-title">Finding the Intersection Line of Two Planes in 3D Space</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="app-subtitle">'
    "Enter the coefficients for two planes in the form "
    "<b>ax₁ + bx₂ + cx₃ = d</b>. "
    "The app computes the intersection line when it exists and visualizes both planes."
    "</div>",
    unsafe_allow_html=True,
)


def latex_plane(a, b, c, d):
    """Build a LaTeX plane equation in the form ax₁ + bx₂ + cx₃ = d."""
    parts = []
    for coef, var in ((a, "x_1"), (b, "x_2"), (c, "x_3")):
        if abs(coef) == 1:
            term = var
        else:
            term = f"{abs(coef):g}{var}"

        if not parts:
            parts.append(term if coef >= 0 else f"-{term}")
        else:
            parts.append(f" + {term}" if coef >= 0 else f" - {term}")

    return "".join(parts) + f" = {d:g}"


col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Plane A")
    a1 = st.number_input("a₁", value=None, placeholder="Enter a", key="a1", format="%f")
    b1 = st.number_input("b₁", value=None, placeholder="Enter b", key="b1", format="%f")
    c1 = st.number_input("c₁", value=None, placeholder="Enter c", key="c1", format="%f")
    d1 = st.number_input("d₁", value=None, placeholder="Enter d", key="d1", format="%f")

with col_b:
    st.subheader("Plane B")
    a2 = st.number_input("a₂", value=None, placeholder="Enter a", key="a2", format="%f")
    b2 = st.number_input("b₂", value=None, placeholder="Enter b", key="b2", format="%f")
    c2 = st.number_input("c₂", value=None, placeholder="Enter c", key="c2", format="%f")
    d2 = st.number_input("d₂", value=None, placeholder="Enter d", key="d2", format="%f")

inputs = [a1, b1, c1, d1, a2, b2, c2, d2]

if any(value is None for value in inputs):
    st.info(
        "Enter all coefficients for both planes in the form "
        "ax₁ + bx₂ + cx₃ = d to compute the intersection."
    )
    st.stop()

plane_a = [a1, b1, c1, d1]
plane_b = [a2, b2, c2, d2]

st.markdown("### Plane Equations")
st.latex(latex_plane(a1, b1, c1, d1))
st.latex(latex_plane(a2, b2, c2, d2))

analysis = analyzePlaneIntersection(plane_a, plane_b)

st.markdown("### Result")
if analysis["case"] == "line":
    st.success(analysis["explanation"])
elif analysis["case"] == "parallel":
    st.warning(analysis["explanation"])
elif analysis["case"] == "coincident":
    st.info(analysis["explanation"])

with st.expander("Show step-by-step RREF calculation", expanded=True):
    for step in analysis["steps"]:
        st.text(step)
        st.divider()

fig, _ = createPlaneVisual(plane_a, plane_b)
st.caption("Drag to rotate · Scroll to zoom · Right-click drag to pan · Double-click to reset view")
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "scrollZoom": True,
        "displaylogo": False,
        "modeBarButtonsToAdd": ["resetCameraDefault3d", "resetCameraLastSave3d"],
    },
)
