# IAPWS‑95 Water Properties (Region 1 Only)

Home Assistant integration providing thermodynamic water properties using the IAPWS‑95 equation of state. Region‑1 only (liquid water; up to approx. 350 °C, up to approx. 100 bar)! This package is based on Python library iapws, version IAPWS‑95 / R6‑95(2018).

## ✅ Features
- Temperature input (°C/K/F)
- Pressure input (bar/psi/Pa/kPa/MPa)
- SI or Imperial output
- Density, enthalpy, entropy, cp, cv, viscosity, thermal conductivity, speed of sound

## ✅ Installation (HACS)
1. Add repository
2. Install integration
3. Configure via UI

## Device with entities in HA (German language)
<img width="1254" height="916" alt="grafik" src="https://github.com/user-attachments/assets/f998fbc6-77d1-4d78-9cdf-1448bf00b11c" />

## Why I developed this integration

I have a heat pump without a heat meter. However, I do have sensors to measure the heat pump’s inlet and outlet temperatures (in °C), system pressure (in bar), and volume flow (in L/min). To calculate the heat flow (in W) and the COP, I need the density and heat capacity of the fluid. On average, the factor is approximately 69 W/K (= density * heat capacity / 60, assuming flow is in L/min). Since both density and heat capacity depend on temperature and pressure, and I was already familiar with the IAPWS, I decided to create this Home Assistant integration.