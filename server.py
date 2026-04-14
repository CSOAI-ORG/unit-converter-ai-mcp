"""Unit Converter AI MCP Server — Unit conversion tools."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import time
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("unit-converter-ai-mcp")
_calls: dict[str, list[float]] = {}
DAILY_LIMIT = 50

def _rate_check(tool: str) -> bool:
    now = time.time()
    _calls.setdefault(tool, [])
    _calls[tool] = [t for t in _calls[tool] if t > now - 86400]
    if len(_calls[tool]) >= DAILY_LIMIT:
        return False
    _calls[tool].append(now)
    return True

LENGTH_TO_METERS = {
    "mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
    "inch": 0.0254, "foot": 0.3048, "yard": 0.9144, "mile": 1609.344,
    "nautical_mile": 1852.0, "light_year": 9.461e15,
}

WEIGHT_TO_KG = {
    "mg": 1e-6, "g": 0.001, "kg": 1.0, "tonne": 1000.0,
    "oz": 0.0283495, "lb": 0.453592, "stone": 6.35029, "ton_us": 907.185, "ton_uk": 1016.05,
}

@mcp.tool()
def convert_length(value: float, from_unit: str, to_unit: str, api_key: str = "") -> dict[str, Any]:
    """Convert between length units: mm, cm, m, km, inch, foot, yard, mile, nautical_mile, light_year."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("convert_length"):
        return {"error": "Rate limit exceeded (50/day)"}
    if from_unit not in LENGTH_TO_METERS or to_unit not in LENGTH_TO_METERS:
        return {"error": f"Unknown unit. Available: {', '.join(LENGTH_TO_METERS)}"}
    meters = value * LENGTH_TO_METERS[from_unit]
    result = meters / LENGTH_TO_METERS[to_unit]
    return {
        "input": value, "from": from_unit, "to": to_unit,
        "result": result, "formula": f"{value} {from_unit} = {result:.6g} {to_unit}",
        "in_meters": meters
    }

@mcp.tool()
def convert_weight(value: float, from_unit: str, to_unit: str, api_key: str = "") -> dict[str, Any]:
    """Convert between weight units: mg, g, kg, tonne, oz, lb, stone, ton_us, ton_uk."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("convert_weight"):
        return {"error": "Rate limit exceeded (50/day)"}
    if from_unit not in WEIGHT_TO_KG or to_unit not in WEIGHT_TO_KG:
        return {"error": f"Unknown unit. Available: {', '.join(WEIGHT_TO_KG)}"}
    kg = value * WEIGHT_TO_KG[from_unit]
    result = kg / WEIGHT_TO_KG[to_unit]
    return {
        "input": value, "from": from_unit, "to": to_unit,
        "result": result, "formula": f"{value} {from_unit} = {result:.6g} {to_unit}",
        "in_kg": kg
    }

@mcp.tool()
def convert_temperature(value: float, from_unit: str, to_unit: str, api_key: str = "") -> dict[str, Any]:
    """Convert between temperature units: celsius, fahrenheit, kelvin, rankine."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("convert_temperature"):
        return {"error": "Rate limit exceeded (50/day)"}
    units = {"celsius", "fahrenheit", "kelvin", "rankine"}
    from_u = from_unit.lower()
    to_u = to_unit.lower()
    if from_u not in units or to_u not in units:
        return {"error": f"Unknown unit. Available: {', '.join(units)}"}
    # Convert to Celsius first
    if from_u == "celsius": c = value
    elif from_u == "fahrenheit": c = (value - 32) * 5 / 9
    elif from_u == "kelvin": c = value - 273.15
    elif from_u == "rankine": c = (value - 491.67) * 5 / 9
    else: c = value
    # Convert from Celsius
    if to_u == "celsius": result = c
    elif to_u == "fahrenheit": result = c * 9 / 5 + 32
    elif to_u == "kelvin": result = c + 273.15
    elif to_u == "rankine": result = (c + 273.15) * 9 / 5
    else: result = c
    return {
        "input": value, "from": from_unit, "to": to_unit,
        "result": round(result, 4), "formula": f"{value}{from_unit[0].upper()} = {round(result, 4)}{to_unit[0].upper()}"
    }

@mcp.tool()
def convert_currency_data(value: float, from_currency: str, to_currency: str, api_key: str = "") -> dict[str, Any]:
    """Convert currency using static reference rates (for estimation only). Use live API for production."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if not _rate_check("convert_currency_data"):
        return {"error": "Rate limit exceeded (50/day)"}
    # Static rates vs USD (approximate)
    rates = {
        "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.5, "AUD": 1.53,
        "CAD": 1.36, "CHF": 0.88, "CNY": 7.24, "INR": 83.1, "NZD": 1.67,
        "SEK": 10.42, "NOK": 10.55, "DKK": 6.87, "SGD": 1.34, "HKD": 7.82,
        "KRW": 1320.0, "BRL": 4.97, "MXN": 17.15, "ZAR": 18.6, "TRY": 30.2,
    }
    fc = from_currency.upper()
    tc = to_currency.upper()
    if fc not in rates or tc not in rates:
        return {"error": f"Unknown currency. Available: {', '.join(sorted(rates))}"}
    usd = value / rates[fc]
    result = usd * rates[tc]
    return {
        "input": value, "from": fc, "to": tc,
        "result": round(result, 2), "rate": round(rates[tc] / rates[fc], 6),
        "via_usd": round(usd, 2),
        "warning": "Static reference rates for estimation. Use live rates for transactions."
    }

if __name__ == "__main__":
    mcp.run()
