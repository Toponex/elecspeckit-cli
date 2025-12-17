---
name: mouser-component-search
description: Search Mouser Electronics for component availability, pricing, datasheets, and lead times. Use when designing hardware, sourcing components, checking inventory, comparing prices, or finding datasheets for electronic parts.
version: 1.0.0
requires_api: true
api_key: ""
---

# mouser-component-search

Search Mouser Electronics for component availability, pricing, datasheets, and lead times.

## Overview

The **mouser-component-search** Skill provides seamless integration with the Mouser Electronics API, enabling you to:

- Search for electronic components by part number, manufacturer, or keyword
- Check real-time inventory availability and stock levels
- Get current pricing information with quantity breaks
- Access datasheet links directly from search results
- View lead times for out-of-stock or backorder items

This Skill is essential for hardware engineers, electronics designers, and anyone working with electronic components who needs to quickly verify component availability and pricing from Mouser Electronics.

## When to Use This Skill

Use the mouser-component-search Skill when you need to:

- **Component Sourcing**: Find where to purchase specific electronic components
- **BOM Validation**: Verify that components in your Bill of Materials are available
- **Price Estimation**: Get cost estimates for component procurement
- **Datasheet Access**: Quickly find official datasheets for components
- **Lead Time Planning**: Check delivery timelines for project planning
- **Alternative Parts**: Search for similar components when your first choice is unavailable

## Usage

The Skill uses a Python script (`scripts/mouser_search.py`) that interfaces with the Mouser Search API.

**Example 1: Search for a microcontroller**
```
Please search Mouser for STM32F103C8T6 and show me the availability and pricing.
```

**Example 2: Check multiple components**
```
I need to check Mouser inventory for these components:
- LM358 op-amp
- 1N4148 diode
- BC547 transistor

Please search each one and summarize the results.
```

**Example 3: Get datasheet link**
```
Find the STM32F407VGT6 on Mouser and provide the datasheet link.
```

## Configuration

### Prerequisites

1. **Mouser API Account**: You must have a Mouser Electronics account and API access
2. **API Key**: Obtain your API key from the Mouser Developer Portal: https://www.mouser.com/api-hub/
3. **Python Dependencies**: The script requires Python 3.11+ with the `requests` library

### API Key Setup

The mouser-component-search Skill requires an API key to access the Mouser Search API. Follow these steps:

#### Step 1: Obtain Your Mouser API Key

1. Visit the Mouser Developer Portal: https://www.mouser.com/api-hub/
2. Log in with your Mouser Electronics account (or create one if needed)
3. Navigate to "My Account" → "API Keys"
4. Generate a new API key for search operations
5. Copy your API key (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

#### Step 2: Configure the Skill

Use the `/elecspeckit.skillconfig update` command to set your API key:

```bash
/elecspeckit.skillconfig update mouser-component-search --api-key YOUR_API_KEY
```

Replace `YOUR_API_KEY` with your actual Mouser API key.

#### Step 3: Enable the Skill

After configuring the API key, enable the Skill:

```bash
/elecspeckit.skillconfig enable mouser-component-search
```

#### Step 4: Verify Configuration

List all Skills to verify the configuration:

```bash
/elecspeckit.skillconfig list
```

You should see `mouser-component-search` with status `enabled: true`.

### Configuration File

The API key is stored in `.elecspecify/memory/skill_config.json`:

```json
{
  "skills": {
    "mouser-component-search": {
      "enabled": true,
      "requires_api": true,
      "api_key": "YOUR_API_KEY",
      "description": "Mouser component availability and pricing search"
    }
  }
}
```

**Security Note**: The `skill_config.json` file should have restricted permissions. Never commit this file to version control or share your API key publicly.

## Response Format

The Skill returns structured JSON data:

### Successful Search

```json
{
  "success": true,
  "results": [
    {
      "part_number": "STM32F103C8T6",
      "manufacturer": "STMicroelectronics",
      "stock": 5000,
      "price": "$2.50",
      "datasheet_url": "https://www.mouser.com/datasheet/...",
      "lead_time": "10 weeks"
    }
  ]
}
```

### No Results Found

```json
{
  "success": true,
  "results": []
}
```

### Error Response

```json
{
  "success": false,
  "error": "API key not configured. Please use /elecspeckit.skillconfig update mouser-component-search --api-key YOUR_KEY to configure"
}
```

## Error Handling

The Skill handles various error scenarios gracefully:

### 1. API Key Not Configured

**Error**: `API key not configured`

**Solution**: Configure your API key using `/elecspeckit.skillconfig update mouser-component-search --api-key YOUR_KEY`

### 2. Invalid API Key

**Error**: `Invalid API key, please check your configuration`

**Solution**: Verify your API key is correct. Generate a new key from the Mouser Developer Portal if needed.

### 3. Rate Limit Exceeded

**Error**: `API rate limit exceeded, please try again later`

**Solution**: Mouser API has rate limits (50 requests/call, 30 calls/min). Wait a few minutes before trying again.

### 4. Network Issues

**Error**: `Unable to connect to Mouser API, please check network connection`

**Solution**: Verify your internet connection and that `api.mouser.com` is accessible from your network.

### 5. No Results

**Behavior**: Returns `"success": true` with empty `results` array

**Meaning**: The search query didn't match any components. Try:
- Checking the spelling of the part number
- Using a more generic search term
- Searching by manufacturer name

## API Limits and Best Practices

### Rate Limits

- **50 requests per call**
- **30 calls per minute**

The Skill automatically handles rate limit errors and provides clear feedback.

### Best Practices

1. **Be Specific**: Use exact part numbers when possible for fastest results
2. **Batch Searches**: If checking multiple components, search them in one conversation to minimize API calls
3. **Cache Results**: Component availability changes slowly; avoid redundant searches
4. **Respect Limits**: Don't implement automated loops that could exceed rate limits

## Technical Details

### Script Location

- **Script**: `scripts/mouser_search.py`
- **Language**: Python 3.11+
- **Dependencies**: `requests>=2.31.0`

### API Endpoint

- **URL**: `https://api.mouser.com/api/v1/search/keyword`
- **Method**: GET
- **Authentication**: API Key (Header: `X-API-Key`)
- **Response Format**: JSON

### Configuration Path

- **Config File**: `~/.elecspecify/memory/skill_config.json`
- **Permissions**: 0600 (Unix-like systems)

## Examples

### Example 1: Basic Component Search

**User Request**:
```
Search Mouser for STM32F103C8T6
```

**Claude Response** (using this Skill):
```
I found the STM32F103C8T6 on Mouser:

- Part Number: STM32F103C8T6
- Manufacturer: STMicroelectronics
- Stock: 5,000 units available
- Price: $2.50 (unit price)
- Datasheet: [View PDF](https://www.mouser.com/datasheet/...)
- Lead Time: 10 weeks

This microcontroller is readily available with good stock levels.
```

### Example 2: Price Comparison

**User Request**:
```
I'm comparing LM358 op-amps from different sources. What's Mouser's price?
```

**Claude Response** (using this Skill):
```
Checking Mouser for LM358 op-amp...

Mouser has LM358 in stock:
- Price: $0.35 per unit
- Stock: 15,000+ units
- Manufacturer: Texas Instruments
- Datasheet: [Available here](...)

This is a commonly stocked part with excellent availability.
```

### Example 3: BOM Validation

**User Request**:
```
I'm finalizing my BOM. Can you check if these parts are available on Mouser?
- STM32F407VGT6
- AMS1117-3.3
- 0805 10uF capacitors
```

**Claude Response** (using this Skill):
```
I'll check each component on Mouser:

1. STM32F407VGT6 (Microcontroller):
   - Stock: 2,500 units
   - Price: $8.50
   - Status: Available

2. AMS1117-3.3 (Voltage Regulator):
   - Stock: 8,000 units
   - Price: $0.45
   - Status: Available

3. 0805 10uF Capacitors:
   - Multiple options available
   - Price range: $0.10 - $0.25
   - Status: Available

All components are currently in stock on Mouser.
```

## Troubleshooting

### Problem: Skill Not Responding

**Check**:
1. Is the Skill enabled? Run `/elecspeckit.skillconfig list`
2. Is the API key configured? Check `.elecspecify/memory/skill_config.json`
3. Is Python 3.11+ installed? Run `python --version`
4. Is the `requests` library installed? Run `pip list | grep requests`

### Problem: "Invalid API Key" Error

**Solutions**:
1. Verify your API key at https://www.mouser.com/api-hub/
2. Check for typos in the API key configuration
3. Generate a new API key if the current one is expired or revoked
4. Reconfigure using `/elecspeckit.skillconfig update mouser-component-search --api-key NEW_KEY`

### Problem: Empty Results for Valid Part Numbers

**Possible Causes**:
1. Part number not available at Mouser (try other distributors)
2. Part number discontinued or obsolete
3. Typo in part number (check manufacturer's website)
4. Part is distributor-specific (not sold through Mouser)

**Solutions**:
- Try broader search terms
- Search by manufacturer name
- Check Mouser's website directly to verify availability

## Version History

- **v1.0.0** (2025-12-16): Initial release
  - Mouser Search API integration
  - Real-time inventory checking
  - Price and datasheet retrieval
  - Error handling for API key issues
  - Rate limit handling

## Related Skills

- **docs-seeker**: Find component datasheets from multiple sources
- **web-research**: Research component specifications and alternatives
- **embedded-systems**: Get guidance on component selection for embedded designs

## Support

For issues specific to this Skill:
- Check the ElecSpeckit documentation: https://github.com/your-org/elecspeckit-cli
- Report bugs: https://github.com/your-org/elecspeckit-cli/issues

For Mouser API issues:
- Mouser Developer Portal: https://www.mouser.com/api-hub/
- Mouser Support: https://www.mouser.com/contact-us/

## License

This Skill follows the ElecSpeckit CLI license. See the main repository LICENSE file.

---

**Last Updated**: 2025-12-16
**Skill Type**: Type 2 (API Integration)
**Status**: Production Ready
