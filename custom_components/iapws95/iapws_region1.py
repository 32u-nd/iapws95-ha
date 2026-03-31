from iapws import IAPWS95


def convert_temperature_to_K(value, unit):
    if unit == "C":
        return value + 273.15
    if unit == "F":
        return (value - 32) * 5 / 9 + 273.15
    return value  # K


def convert_pressure_to_MPa(value, unit):
    if unit == "bar":
        return value / 10
    if unit == "psi":
        return value * 0.00689476
    if unit == "kPa":
        return value / 1000
    if unit == "Pa":
        return value / 1_000_000
    return value  # MPa


def convert_output_si(state):
    return {
        "density": state.rho,  # kg/m3
        "enthalpy": state.h,  # kJ/kg
        "entropy": state.s,  # kJ/kgK
        "internal_energy": state.u,  # kJ/kg
        "cp": state.cp,  # kJ/kgK
        "cv": state.cv,  # kJ/kgK
        "speed_of_sound": state.w,  # m/s
        "viscosity": state.mu,  # Pa*s
        "thermal_conductivity": state.k,  # W/mK
    }


def convert_output_imperial(si):
    return {
        "density": si["density"] * 0.062428,  # kg/m3 → lb/ft3
        "enthalpy": si["enthalpy"] * 0.43021,  # kJ/kg → BTU/lbm
        "entropy": si["entropy"] * 0.238845,  # kJ/kgK → BTU/lbm°F
        "internal_energy": si["internal_energy"] * 0.43021,
        "cp": si["cp"] * 0.238845,
        "cv": si["cv"] * 0.238845,
        "speed_of_sound": si["speed_of_sound"] * 3.28084,
        "viscosity": si["viscosity"] * 0.020885,  # Pa*s → lb/(ft*s)
        "thermal_conductivity": si["thermal_conductivity"] * 0.577789,
    }


def compute_region1(T_input, P_input, T_unit, P_unit, out_unit):
    T_K = convert_temperature_to_K(T_input, T_unit)
    P_MPa = convert_pressure_to_MPa(P_input, P_unit)

    state = IAPWS95(T=T_K, P=P_MPa)

    si = convert_output_si(state)

    if out_unit == "imperial":
        return convert_output_imperial(si)
    else:
        return si
