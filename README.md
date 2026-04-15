# Unit Converter Ai

> By [MEOK AI Labs](https://meok.ai) — MEOK AI Labs MCP Server

Unit Converter AI MCP Server — Unit conversion tools.

## Installation

```bash
pip install unit-converter-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install unit-converter-ai-mcp
```

## Tools

### `convert_length`
Convert between length units: mm, cm, m, km, inch, foot, yard, mile, nautical_mile, light_year.

**Parameters:**
- `value` (float)
- `from_unit` (str)
- `to_unit` (str)

### `convert_weight`
Convert between weight units: mg, g, kg, tonne, oz, lb, stone, ton_us, ton_uk.

**Parameters:**
- `value` (float)
- `from_unit` (str)
- `to_unit` (str)

### `convert_temperature`
Convert between temperature units: celsius, fahrenheit, kelvin, rankine.

**Parameters:**
- `value` (float)
- `from_unit` (str)
- `to_unit` (str)

### `convert_currency_data`
Convert currency using static reference rates (for estimation only). Use live API for production.

**Parameters:**
- `value` (float)
- `from_currency` (str)
- `to_currency` (str)


## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## Links

- **Website**: [meok.ai](https://meok.ai)
- **GitHub**: [CSOAI-ORG/unit-converter-ai-mcp](https://github.com/CSOAI-ORG/unit-converter-ai-mcp)
- **PyPI**: [pypi.org/project/unit-converter-ai-mcp](https://pypi.org/project/unit-converter-ai-mcp/)

## License

MIT — MEOK AI Labs
