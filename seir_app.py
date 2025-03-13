import streamlit as st  
import numpy as np  
import matplotlib.pyplot as plt  

st.set_page_config(page_title="Norfolk Schools & Surrounding Area SEIR Model Simulator", layout="wide")  
   
st.title("Norfolk Schools & Surrounding Area SEIR Model Simulator")  
st.write("VDH - Measels Outbreak Simulation.")  
   
# Sidebar controls for parameters  
N = st.sidebar.number_input("Total number of students", value=500)  
vaccination_rate = st.sidebar.slider("Vaccination rate (%)", 0, 100, 95) / 100  
initial_infected = st.sidebar.number_input("Initial number of infected students", value=1)  
beta = st.sidebar.slider("Transmission rate (β)", 12.0, 18.0, 15.0, step=0.1) 
latent_period = st.sidebar.number_input("Latent period (days)", value=8)  
infectious_period = st.sidebar.number_input("Infectious period (days)", value=5)  
days_to_simulate = st.sidebar.number_input("Simulation days", value=30)  
   
time_step = 0.1  
   
#  initial conditionss
vaccinated_students = int(N * vaccination_rate)  
S0 = N - vaccinated_students - initial_infected  
E0 = 0  
I0 = initial_infected  
R0 = vaccinated_students  
   
sigma = 1 / latent_period  
gamma = 1 / infectious_period  
   
total_steps = int(days_to_simulate / time_step)  
time = np.linspace(0, days_to_simulate, total_steps + 1)  
   
# Initializing arrays  
S = np.zeros(total_steps + 1)  
E = np.zeros(total_steps + 1)  
I = np.zeros(total_steps + 1)  
R = np.zeros(total_steps + 1)  
   
S[0] = S0  
E[0] = E0  
I[0] = I0  
R[0] = R0  
   
#  τ‐leap method for stochastic simulation - POI
for t in range(total_steps):  
     lambda_SE = beta * S[t] * I[t] / N * time_step  
     lambda_EI = sigma * E[t] * time_step  
     lambda_IR = gamma * I[t] * time_step  
   
     # Sample events from Poisson distributions  
     n_SE = np.random.poisson(lambda_SE)  
     n_EI = np.random.poisson(lambda_EI)  
     n_IR = np.random.poisson(lambda_IR)  
   
     # Events aren't greater than available individuals  
     n_SE = min(n_SE, S[t])  
     n_EI = min(n_EI, E[t])  
     n_IR = min(n_IR, I[t])  
   
     S[t+1] = S[t] - n_SE  
     E[t+1] = E[t] + n_SE - n_EI  
     I[t+1] = I[t] + n_EI - n_IR  
     R[t+1] = R[t] + n_IR  
   
# Plot results  
fig, ax = plt.subplots(figsize=(9, 6))  
ax.plot(time, S, label="Susceptible", color="#766CDB", linewidth=2)  
ax.plot(time, E, label="Exposed", color="#DA847C", linewidth=2)  
ax.plot(time, I, label="Infectious", color="#7CD9A5", linewidth=2)  
ax.plot(time, R, label="Recovered", color="#52515E", linewidth=2)  
   
ax.set_title("Norfolk Measles Model Simulation", pad=15, fontsize=20, fontweight="semibold", color="#222222")  
ax.set_xlabel("Time (days)", labelpad=10, fontsize=16, fontweight="medium", color="#333333")  
ax.set_ylabel("Number of Students", labelpad=10, fontsize=16, fontweight="medium", color="#333333")  
ax.tick_params(axis="both", labelsize=14, colors="#555555")  
ax.grid(color="#E0E0E0")  
ax.legend(fontsize=12, frameon=False, loc="upper right")  
ax.set_axisbelow(True)  
   
st.pyplot(fig)  
   
st.write("Simulation complete!")  
