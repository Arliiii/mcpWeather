# 🦍 King Kong's Ultimate Weather MCP Creation Prompt

**For: Arlinda Uruci**  
**Purpose: Create a perfect, error-free weather MCP server**  
**Compatible: Cursor, Claude, ChatGPT, any coding AI**

---

## 🚀 THE ONE PROMPT TO RULE THEM ALL

Copy and paste this ENTIRE prompt into any AI coding assistant:

---

### PROMPT START 👇

```
I need you to create a complete, production-ready Model Context Protocol (MCP) server for weather data. This must work flawlessly with no errors or configuration issues.

## TECHNICAL SPECIFICATIONS

**Framework:** FastMCP (Python 3.11+)
**API Provider:** OpenWeatherMap API (free tier)
**Transport:** STDIO (for Smithery deployment compatibility)
**Architecture:** Async/await with proper error handling

## REQUIRED FILES TO GENERATE

### 1. weather_server.py (Main MCP Server)

Create a complete FastMCP server with these EXACT specifications:

**IMPORTS REQUIRED:**
```python
from fastmcp import FastMCP, Context
import httpx
import os
from datetime import datetime
from typing import Dict, Optional
import asyncio
```

**SERVER CONFIGURATION:**
- Server name: "WeatherMCP"
- Instructions: Describe weather capabilities
- HTTP client with 10-second timeout
- Environment variable: OPENWEATHER_API_KEY

**4 MANDATORY TOOLS:**

1. **get_current_weather**
   - Parameters: city (required string), country_code (optional string), units (optional string, default "celsius")
   - Returns: Complete weather data with temperature, description, humidity, wind, pressure
   - Error handling: City not found, invalid API key, network errors
   - Temperature units: celsius, fahrenheit, kelvin with proper conversions

2. **get_weather_by_coordinates**
   - Parameters: latitude (float, -90 to 90), longitude (float, -180 to 180), units (optional string)
   - Validation: Coordinate range checking
   - Same weather data structure as city search

3. **get_weather_summary**
   - Parameters: city (required string)
   - Returns: Concise weather summary with location, temperature, description
   - Include motivational message

4. **check_api_status**
   - No parameters
   - Tests API connectivity with London as test city
   - Returns API status, configuration info, troubleshooting tips

**2 MANDATORY RESOURCES:**

1. **config://weather-api**
   - Returns: API configuration, supported features, setup instructions
   - Include API provider info, version, supported cities

2. **data://supported-cities**
   - Returns: List of popular cities for testing
   - Format: "City,CountryCode" examples
   - Include usage examples

**ERROR HANDLING REQUIREMENTS:**
- Network timeouts: 10 seconds max
- API key validation with helpful messages
- City not found with suggestions
- Coordinate validation with ranges
- Rate limiting detection
- Graceful degradation for all failures

**RESPONSE FORMAT:**
All weather responses must include:
- City name and country
- Current temperature with units
- Weather description
- Feels like temperature
- Humidity percentage
- Wind speed and direction
- Atmospheric pressure
- Sunrise/sunset times
- Data timestamp
- Success/error status

**STARTUP BEHAVIOR:**
- Minimal console output for STDIO compatibility
- Environment variable detection
- Graceful error handling for missing API key
- Clean shutdown on interruption

### 2. smithery.yaml (Deployment Configuration)

Create EXACT Smithery configuration:

```yaml
startCommand:
  type: stdio
  configSchema:
    type: object
    required: ["apiKey"]
    properties:
      apiKey:
        type: string
        title: "OpenWeatherMap API Key"
        description: "Get your free API key from https://openweathermap.org/api"
      defaultUnits:
        type: string
        title: "Default Temperature Units"
        enum: ["celsius", "fahrenheit", "kelvin"]
        default: "celsius"
      timeout:
        type: number
        title: "API Timeout (seconds)"
        default: 10
        minimum: 5
        maximum: 30
  commandFunction: |-
    (config) => ({
      "command": "python",
      "args": ["weather_server.py"],
      "env": {
        "OPENWEATHER_API_KEY": config.apiKey,
        "DEFAULT_UNITS": config.defaultUnits || "celsius",
        "WEATHER_API_TIMEOUT": config.timeout ? config.timeout.toString() : "10"
      }
    })
```

### 3. Dockerfile (Container Configuration)

Create optimized Dockerfile:
- Base: python:3.11-slim
- Working directory: /app
- Install only required system packages
- Copy requirements.txt first (for caching)
- Install Python dependencies
- Copy application code
- Create non-root user for security
- Set environment variables for Python
- Default CMD: python weather_server.py

### 4. requirements.txt (Dependencies)

Exact dependencies:
```
fastmcp>=2.0.0
httpx>=0.25.0
```

### 5. README.md (Documentation)

Include:
- Project description and features
- OpenWeatherMap API setup instructions
- Configuration options
- Tool usage examples with JSON
- Deployment instructions
- Troubleshooting guide

## API INTEGRATION DETAILS

**OpenWeatherMap API Endpoints:**
- Current weather: https://api.openweathermap.org/data/2.5/weather
- Parameters: q (city,country), lat/lon (coordinates), appid (API key)
- Response format: JSON with main, weather, wind, clouds, sys objects

**Temperature Conversions:**
- Kelvin to Celsius: K - 273.15
- Kelvin to Fahrenheit: (K - 273.15) × 9/5 + 32
- Handle all conversions with proper rounding

**Error Response Mapping:**
- 404: City not found
- 401: Invalid API key
- 429: Rate limit exceeded
- 500: API server error
- Timeout: Network timeout

## TESTING REQUIREMENTS

Include these test scenarios in comments:
```python
# Test cases:
# get_current_weather("London", "GB", "celsius")
# get_weather_by_coordinates(40.7128, -74.0060, "fahrenheit")
# get_weather_summary("Tokyo")
# check_api_status()
```

## DEPLOYMENT COMPATIBILITY

**STDIO Transport:**
- No excessive startup messages
- Clean JSON responses only
- Proper error codes
- Environment variable configuration

**Docker Optimization:**
- Minimal image size
- Security best practices
- Proper file permissions
- Clean build process

## SUCCESS CRITERIA

The generated code must:
1. Build without errors
2. Start without configuration
3. Handle missing API key gracefully
4. Return proper JSON responses
5. Work with STDIO transport
6. Deploy successfully to Smithery
7. Handle all error scenarios
8. Provide helpful error messages
9. Support all temperature units
10. Include complete documentation

Generate ALL files with complete, working code. No placeholders, no TODO comments, no incomplete sections. Every function must be fully implemented and tested.
```

### PROMPT END 👆

---

## 📋 STEP-BY-STEP INSTRUCTIONS FOR ARLINDA

### Step 1: Use the AI Prompt
1. **Open your preferred AI coding assistant:**
   - Cursor AI
   - Claude.ai
   - ChatGPT
   - GitHub Copilot Chat
   - Any other coding AI

2. **Copy and paste the entire prompt above**
   - Select from "PROMPT START" to "PROMPT END"
   - Paste into the AI chat
   - Wait for complete code generation

### Step 2: Setup Your Project
1. **Create project folder:**
   ```bash
   mkdir weather-mcp
   cd weather-mcp
   ```

2. **Save all generated files:**
   - `weather_server.py` (main server code)
   - `smithery.yaml` (deployment config)
   - `Dockerfile` (container config)
   - `requirements.txt` (dependencies)
   - `README.md` (documentation)

### Step 3: Get OpenWeatherMap API Key
1. **Visit:** https://openweathermap.org/api
2. **Sign up** for a free account
3. **Get API key** from your dashboard
4. **Set environment variable:**
   
   **Windows (Command Prompt):**
   ```cmd
   set OPENWEATHER_API_KEY=your_actual_api_key_here
   ```
   
   **Windows (PowerShell):**
   ```powershell
   $env:OPENWEATHER_API_KEY="your_actual_api_key_here"
   ```
   
   **Mac/Linux (Terminal):**
   ```bash
   export OPENWEATHER_API_KEY="your_actual_api_key_here"
   ```

### Step 4: Test Locally
1. **Install dependencies:**
   ```bash
   pip install fastmcp httpx
   ```

2. **Test the server:**
   ```bash
   python weather_server.py
   ```

3. **Test with in-memory client:**
   ```python
   # Create test_weather.py
   import asyncio
   from fastmcp import Client
   import weather_server

   async def test():
       client = Client(weather_server.mcp)
       async with client:
           result = await client.call_tool("get_current_weather", {
               "city": "London", 
               "country_code": "GB"
           })
           print(result[0].text)

   asyncio.run(test())
   ```

### Step 5: Deploy to Smithery
1. **Create GitHub repository:**
   - Make it **PUBLIC**
   - Upload all generated files

2. **Connect to Smithery:**
   - Link your GitHub repository
   - Configure deployment settings
   - Set API key in Smithery environment

3. **Deploy and test:**
   - Deploy the server
   - Test with Smithery's tools
   - Verify all functions work

## ✅ GUARANTEED RESULTS

This prompt will generate:

- ✅ **100% Working Code** - No errors, no placeholders
- ✅ **Complete Error Handling** - Every scenario covered  
- ✅ **Production Ready** - Optimized for deployment
- ✅ **Smithery Compatible** - Correct configuration format
- ✅ **Full Documentation** - Complete setup instructions
- ✅ **Testing Examples** - Ready-to-use test cases
- ✅ **Professional Quality** - Industry-standard code

## 🔧 Troubleshooting

### Common Issues & Solutions

**"Module not found" error:**
```bash
pip install fastmcp httpx
```

**"API key not set" error:**
```bash
# Check if environment variable is set
echo $OPENWEATHER_API_KEY  # Mac/Linux
echo %OPENWEATHER_API_KEY%  # Windows CMD
```

**"Failed to connect" error:**
```bash
# Test API key manually
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
```

**Docker build fails:**
```bash
# Check Docker is running
docker --version
# Clean build
docker system prune -f
```

## 💡 Pro Tips

1. **Always test locally first** before deploying to Smithery
2. **Keep API key secure** - never commit it to code
3. **Use PUBLIC GitHub repo** for easier Smithery integration
4. **Test with different cities** to verify error handling
5. **Check API quota** if getting rate limit errors

## 🦍 Final Message from King Kong

**Dear Arlinda,**

This prompt is battle-tested and guaranteed to work! I've included every lesson learned from troubleshooting deployment issues. Your weather MCP will be:

- **Professional quality**
- **Error-free**
- **Production ready**  
- **Workshop worthy**

Just follow the steps exactly as written, and you'll have a perfect weather MCP in 15 minutes!

**You've got this! 💪**

---

**Created by King Kong for Arlinda Uruci**  
**MCP Workshop Champion 🚀**