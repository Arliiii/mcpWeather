# 🌤️ WeatherMCP - Professional Weather MCP Server

A production-ready Model Context Protocol (MCP) server for weather data using OpenWeatherMap API.

## ✨ Features

- **Current Weather**: Get weather by city name or coordinates
- **Temperature Units**: Support for Celsius, Fahrenheit, and Kelvin
- **Weather Summaries**: Concise summaries with motivational messages
- **API Status**: Built-in connectivity testing and troubleshooting
- **Error Handling**: Comprehensive error handling with helpful messages
- **STDIO Transport**: Compatible with Smithery and other MCP clients
- **Docker Support**: Containerized deployment ready

## 🚀 Quick Start

### 1. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap API](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Wait up to 10 minutes for activation

### 2. Configure API Key

**Option A: Use .env file (Recommended)**
Create a `.env` file in the project directory:
```env
OPENWEATHER_API_KEY=your_actual_api_key_here
DEFAULT_UNITS=celsius
WEATHER_API_TIMEOUT=10
```

**Option B: Set Environment Variable**

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

### 3. Install Dependencies

```bash
pip install fastmcp httpx
```

### 4. Run the Server

```bash
python weather_server.py
```

## 🛠️ Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key (required) | None |
| `DEFAULT_UNITS` | Default temperature units | `celsius` |
| `WEATHER_API_TIMEOUT` | API timeout in seconds | `10` |

## 📡 Available Tools

### 1. get_current_weather

Get current weather for a city.

**Parameters:**
- `city` (string, required): City name
- `country_code` (string, optional): ISO 3166 country code (e.g., 'GB', 'US')
- `units` (string, optional): Temperature units - celsius, fahrenheit, or kelvin

**Example:**
```json
{
  "city": "London",
  "country_code": "GB",
  "units": "celsius"
}
```

### 2. get_weather_by_coordinates

Get current weather by geographic coordinates.

**Parameters:**
- `latitude` (float, required): Latitude (-90 to 90)
- `longitude` (float, required): Longitude (-180 to 180)
- `units` (string, optional): Temperature units

**Example:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "units": "fahrenheit"
}
```

### 3. get_weather_summary

Get a concise weather summary with motivational message.

**Parameters:**
- `city` (string, required): City name

**Example:**
```json
{
  "city": "Tokyo"
}
```

### 4. check_api_status

Check OpenWeatherMap API connectivity and configuration.

**Parameters:** None

## 📚 Available Resources

### config://weather-api

Returns API configuration, supported features, and setup instructions.

### data://supported-cities

Returns list of popular cities for testing with usage examples.

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t weather-mcp .
```

### Run Container

```bash
docker run -e OPENWEATHER_API_KEY=your_api_key weather-mcp
```

## 🔧 Troubleshooting

### Common Issues

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

### API Status Codes

- `200`: Success
- `401`: Invalid API key
- `404`: City not found
- `429`: Rate limit exceeded
- `500`: Server error

### Rate Limits

- **Free Tier**: 60 calls/minute, 1,000,000 calls/month
- **Paid Tiers**: Higher limits available

## 📋 Testing

Use the built-in `check_api_status` tool to verify your setup:

```python
# Test the API status
result = await client.call_tool("check_api_status", {})
print(result)
```

## 🌍 Supported Cities

The server supports all major cities worldwide. For best results:

- Include country code for accuracy
- Use English city names
- Check spelling if city not found
- Use ISO 3166-1 alpha-2 country codes (GB, US, JP, etc.)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Use the `check_api_status` tool
3. Verify your API key is active
4. Check OpenWeatherMap service status
"# mcp" 
