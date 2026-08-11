import numpy as np

def rref(matrix):
    # computes the reduced row echelon form of a matrix
    rref_matrix = matrix.astype(float)
    rows, cols = rref_matrix.shape
    pivot = 0

    # helper for subscript formatting
    SUB_DIGITS = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')

    # improved display for initial linear equations - specific terms only
    equations_str_parts = []
    for r in range(rows):
        terms = []
        for c in range(cols - 1):
            val = rref_matrix[r, c]
            if val == 0:
                continue

            var = f"x{str(c+1).translate(SUB_DIGITS)}"

            # formatting the term based on the coefficient value
            if val == 1:
                term = f" + {var}"
            elif val == -1:
                term = f" - {var}"
            else:
                sign = " + " if val > 0 else " - "
                mag = f"{abs(val):.0f}" if abs(val) == int(abs(val)) else f"{abs(val):.4f}"
                term = f"{sign}{mag}{var}"
            terms.append(term)

        if not terms:
            eq_str = "0"
        else:
            # join terms and strip leading plus sign if it exists
            eq_str = "".join(terms).strip()
            if eq_str.startswith("+"):
                eq_str = eq_str[1:].strip()
            elif eq_str.startswith("- "):
                eq_str = "-" + eq_str[2:]

        rhs_val = rref_matrix[r, cols-1]
        rhs_str = f"{rhs_val:.0f}" if rhs_val == int(rhs_val) else f"{rhs_val:.4f}"
        equations_str_parts.append(f"{eq_str} = {rhs_str}")

    initial_equations_display = "\n".join(equations_str_parts)
    steps = [f"The linear equations are:\n{initial_equations_display}\n\nCurrent Augmented Matrix:\n" + str(np.round(rref_matrix, 4))]

    for r in range(rows):
        if pivot >= cols:
            break
        i = r
        while rref_matrix[i, pivot] == 0:
            i += 1
            if i == rows:
                i = r
                pivot += 1
                if pivot == cols:
                    for contradiction_row in range(r, rows):
                        if np.all(np.isclose(rref_matrix[contradiction_row, :cols-1], 0)) and not np.isclose(rref_matrix[contradiction_row, cols-1], 0):
                            steps.append("Contradiction found: System has no solution.")
                            break
                    return rref_matrix, steps

        rref_matrix[[i, r]] = rref_matrix[[r, i]]
        pivot_val = rref_matrix[r, pivot]
        rref_matrix[r] = rref_matrix[r] / pivot_val
        steps.append(f"Normalize pivot at row {r+1}:\n" + str(np.round(rref_matrix, 4)))

        for i in range(rows):
            if i != r:
                factor = rref_matrix[i, pivot]
                subscripted_col_idx = str(pivot + 1).translate(SUB_DIGITS)
                rref_matrix[i] = rref_matrix[i] - factor * rref_matrix[r]
                steps.append(f"Eliminate x{subscripted_col_idx} in row {i+1}:\n" + str(np.round(rref_matrix, 4)))
        pivot += 1

    for contradiction_row in range(rows):
        if np.all(np.isclose(rref_matrix[contradiction_row, :cols-1], 0)) and not np.isclose(rref_matrix[contradiction_row, cols-1], 0):
            steps.append("Contradiction found: System has no solution.")
            break

    return rref_matrix, steps

def analyzePlaneIntersection(planeA, planeB):
    augmented_matrix = np.array([planeA, planeB], dtype=float)
    rref_matrix, math_steps = rref(augmented_matrix)

    normalA = np.array(planeA[:3])
    normalB = np.array(planeB[:3])
    rank_a = np.linalg.matrix_rank(augmented_matrix[:, :3])
    rank_aug = np.linalg.matrix_rank(augmented_matrix)
    direction_vector = np.cross(normalA, normalB)
    result = {"normalA": normalA, "normalB": normalB, "directionVector": direction_vector, "rrefMatrix": rref_matrix, "steps": math_steps}

    if rank_a == 2:
        result["case"] = "line"
        result["explanation"] = "The normal vectors are not parallel. The planes intersect at a unique line."
    elif rank_a == 1 and rank_aug == 2:
        result["case"] = "parallel"
        result["explanation"] = "The normal vectors are parallel but the planes have no common points. They are parallel and distinct."
    elif rank_a == 1 and rank_aug == 1:
        result["case"] = "coincident"
        result["explanation"] = "The equations represent the same plane. Every point on one plane is on the other."
    return result

import plotly.graph_objects as go
import numpy as np

def createPlaneVisual(planeA, planeB):
    analysis = analyzePlaneIntersection(planeA, planeB)

    fig = go.Figure()
    x = np.linspace(-10, 10, 20)
    y = np.linspace(-10, 10, 20)
    X, Y = np.meshgrid(x, y)

    def get_z(p, X_grid, Y_grid):
        # calculate z coordinates based on plane parameters
        a, b, c, d = p
        if c != 0:
            return (d - a*X_grid - b*Y_grid) / c
        return np.zeros_like(X_grid)

    # plotting plane a
    fig.add_trace(go.Surface(x=X, y=Y, z=get_z(planeA, X, Y), name="Plane A", colorscale='Blues', showscale=False, opacity=0.7))

    # plotting plane b
    fig.add_trace(go.Surface(x=X, y=Y, z=get_z(planeB, X, Y), name="Plane B", colorscale='Reds', showscale=False, opacity=0.7))

    if analysis['case'] == "line":
        # finding a point on the line using rref
        rref = analysis['rrefMatrix']
        t = np.linspace(-15, 15, 100)
        v = analysis['directionVector']

        # finding a particular solution p0
        p0 = np.zeros(3)
        if rref[0, 0] == 1 and rref[1, 1] == 1:
             p0[0] = rref[0, 3]
             p0[1] = rref[1, 3]
             p0[2] = 0

        line_x = p0[0] + t * v[0]
        line_y = p0[1] + t * v[1]
        line_z = p0[2] + t * v[2]

        fig.add_trace(go.Scatter3d(x=line_x, y=line_y, z=line_z, mode='lines', line=dict(color='yellow', width=8), name="Intersection Line"))

    fig.update_layout(
        template="plotly_dark",
        title=dict(
            text="3D Plane Intersection Visualization",
            x=0.5,
            xanchor="center",
        ),
        height=750,
        scene=dict(
            xaxis_title="x₁",
            yaxis_title="x₂",
            zaxis_title="x₃",
            aspectmode="cube",
        ),
        margin=dict(l=0, r=0, b=0, t=60)
    )
    return fig, analysis
