import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sr-Nd Evolution", layout="wide")

st.title("Sr-Nd Isotope Evolution")

# -----------------------
# Constants
# -----------------------

t = np.linspace(0, 4.6, 300)

rb_const = np.log(2) / 49.610
sm_const = np.log(2) / 106.000

rb_in = 100
sr_in = 0
sm_in = 100
nd_in = 0

smratio = 0.1967
ndratio = 0.5126
rbratio = 0.0839
srratio = 0.7045

d_rb = 0.001
d_sr = 0.03
d_sm = 0.05
d_nd = 0.01

# -----------------------
# Sidebar
# -----------------------

st.sidebar.header("Controls")

seltime = st.sidebar.slider(
    "Time (Ga)",
    0.0,
    4.6,
    2.0,
    0.01,
)

cry = st.sidebar.slider(
    "Melt Event (Ga)",
    0.0,
    4.6,
    1.0,
    0.01,
)

melt = st.sidebar.slider(
    "Melt Percentage",
    0,
    100,
    20,
)

# -----------------------
# Evolution curves
# -----------------------

rb_curr = rbratio * (np.exp(rb_const * (4.6 - t)) - 1)
sr_curr = srratio - rbratio * (np.exp(rb_const * (4.6 - t)) - 1)

sm_curr = smratio * (np.exp(sm_const * (4.6 - t)) - 1)
nd_curr = ndratio - smratio * (np.exp(sm_const * (4.6 - t)) - 1)

# -----------------------
# Figure
# -----------------------

fig = plt.figure(figsize=(18, 12))

ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,1,2)

# -----------------------
# Plot 1
# -----------------------

ax1.plot(t, rb_curr, label="Rb", color="blue")
ax1.plot(t, sr_curr, label="Sr", color="red")

ax1.set_title("Rb-Sr System")
ax1.set_xlabel("Time (Ga)")
ax1.set_ylabel("Ratio")
ax1.grid(True)
ax1.legend()

ax1.axvline(seltime, color="green", linestyle="--")

# -----------------------
# Plot 2
# -----------------------

ax2.plot(t, sm_curr, label="Sm", color="purple")
ax2.plot(t, nd_curr, label="Nd", color="orange")

ax2.set_title("Sm-Nd System")
ax2.set_xlabel("Time (Ga)")
ax2.set_ylabel("Ratio")
ax2.grid(True)
ax2.legend()

ax2.axvline(seltime, color="green", linestyle="--")

# -----------------------
# Plot 3
# -----------------------

ax3.set_title("εNd vs 87Sr/86Sr")

ax3.set_xlabel("87Sr/86Sr")
ax3.set_ylabel("εNd")

ax3.set_xlim(0.698,0.710)
ax3.set_ylim(-10,20)

ax3.axhline(0,color="gray",linestyle=":")

ndevo = ndratio - smratio * (np.exp(sm_const * (4.6 - seltime)) - 1)
srevo = srratio - rbratio * (np.exp(rb_const * (4.6 - seltime)) - 1)

ax3.axvline(srevo,color="gray",linestyle=":")

if cry >= seltime:

    ax3.plot(srevo,0,"rx",markersize=10,label="Melt")
    ax3.plot(srevo,0,"bx",markersize=10,label="Restite")

else:

    time = seltime - cry

    melt_frac = melt/100

    smratioevent = smratio * np.exp(sm_const * (4.6-cry))
    ndratioevent = ndratio - smratio*(np.exp(sm_const*(4.6-cry))-1)

    rbratioevent = rbratio*np.exp(rb_const*(4.6-cry))
    srratioevent = srratio-rbratio*(np.exp(rb_const*(4.6-cry))-1)

    meltsmratio = smratioevent*((d_nd+melt_frac*(1-d_nd))/(d_sm+melt_frac*(1-d_sm)))
    meltrbratio = rbratioevent*((d_sr+melt_frac*(1-d_sr))/(d_rb+melt_frac*(1-d_rb)))

    restitesmratio = meltsmratio*(d_sm/d_nd)
    restiterbratio = meltrbratio*(d_rb/d_sr)

    plotsrratiomelt = srratioevent + meltrbratio*(np.exp(rb_const*time)-1)
    plotsrratiorestite = srratioevent + restiterbratio*(np.exp(rb_const*time)-1)

    nd_melt_current = ndratioevent + meltsmratio*(np.exp(sm_const*time)-1)
    nd_restite_current = ndratioevent + restitesmratio*(np.exp(sm_const*time)-1)

    plotepsmelt = 1000*((nd_melt_current/ndevo)-1)
    plotepsrestite = 1000*((nd_restite_current/ndevo)-1)

    ax3.plot(
        plotsrratiomelt,
        plotepsmelt,
        "rx",
        markersize=10,
        label="Melt"
    )

    ax3.plot(
        plotsrratiorestite,
        plotepsrestite,
        "bx",
        markersize=10,
        label="Restite"
    )

ax3.legend()

plt.tight_layout()

st.pyplot(fig)