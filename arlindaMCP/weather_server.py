from fastmcp import FastMCP
import httpx
import os
from datetime import datetime
from typing import Optional
import asyncio
import json
import signal
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("WeatherMCP")

# Global HTTP client
http_client: Optional[httpx.AsyncClient] = None

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_UNITS = os.getenv("DEFAULT_UNITS", "celsius")
API_TIMEOUT = int(os.getenv("WEATHER_API_TIMEOUT", "10"))

@mcp.tool()
async def get_current_weather(
    city: str,
    country_code: Optional[str] = None,
    units: Optional[str] = "celsius"
) -> str:
    """
    Get current weather for a city.

    Args:
        city: City name (required)
        country_code: ISO 3166 country code (optional, e.g., 'GB', 'US')
        units: Temperature units - celsius, fahrenheit, or kelvin (default: celsius)

    Returns:
        JSON string with complete weather data
    """
    try:
        # Ensure HTTP client is initialized
        if http_client is None:
            await setup_http_client()

        if not API_KEY:
            return json.dumps({
                "error": "API key not configured",
                "message": "Please set OPENWEATHER_API_KEY environment variable",
                "status": "error"
            })

        # Validate units
        valid_units = ["celsius", "fahrenheit", "kelvin"]
        if units not in valid_units:
            units = "celsius"

        # Build query string
        query = city
        if country_code:
            query = f"{city},{country_code}"

        # API units mapping
        api_units = "metric" if units == "celsius" else "imperial" if units == "fahrenheit" else "standard"

        # Make API request
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": query,
            "appid": API_KEY,
            "units": api_units
        }

        response = await http_client.get(url, params=params, timeout=API_TIMEOUT)

        if response.status_code == 404:
            return json.dumps({
                "error": "City not found",
                "message": f"Could not find weather data for '{city}'. Please check the city name and try again.",
                "suggestions": "Try including the country code (e.g., 'London,GB')",
                "status": "error"
            })
        elif response.status_code == 401:
            return json.dumps({
                "error": "Invalid API key",
                "message": "The provided OpenWeatherMap API key is invalid",
                "status": "error"
            })
        elif response.status_code == 429:
            return json.dumps({
                "error": "Rate limit exceeded",
                "message": "API rate limit exceeded. Please try again later.",
                "status": "error"
            })

        response.raise_for_status()
        data = response.json()

        # Convert temperature if needed
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        if units == "kelvin" and api_units != "standard":
            if api_units == "metric":
                temp = temp + 273.15
                feels_like = feels_like + 273.15
            else:  # imperial
                temp = (temp - 32) * 5/9 + 273.15
                feels_like = (feels_like - 32) * 5/9 + 273.15

        # Format response
        result = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(temp, 1),
            "feels_like": round(feels_like, 1),
            "units": units,
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"].get("speed", 0),
            "wind_direction": data["wind"].get("deg", 0),
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S"),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S"),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }

        return json.dumps(result, indent=2)

    except httpx.TimeoutException:
        return json.dumps({
            "error": "Request timeout",
            "message": "Weather API request timed out. Please try again.",
            "status": "error"
        })
    except Exception as e:
        return json.dumps({
            "error": "Unexpected error",
            "message": str(e),
            "status": "error"
        })

@mcp.tool()
async def get_weather_by_coordinates(
    latitude: float,
    longitude: float,
    units: Optional[str] = "celsius"
) -> str:
    """
    Get current weather by geographic coordinates.

    Args:
        latitude: Latitude (-90 to 90)
        longitude: Longitude (-180 to 180)
        units: Temperature units - celsius, fahrenheit, or kelvin (default: celsius)

    Returns:
        JSON string with complete weather data
    """
    try:
        # Ensure HTTP client is initialized
        if http_client is None:
            await setup_http_client()

        if not API_KEY:
            return json.dumps({
                "error": "API key not configured",
                "message": "Please set OPENWEATHER_API_KEY environment variable",
                "status": "error"
            })

        # Validate coordinates
        if not (-90 <= latitude <= 90):
            return json.dumps({
                "error": "Invalid latitude",
                "message": "Latitude must be between -90 and 90 degrees",
                "status": "error"
            })

        if not (-180 <= longitude <= 180):
            return json.dumps({
                "error": "Invalid longitude",
                "message": "Longitude must be between -180 and 180 degrees",
                "status": "error"
            })

        # Validate units
        valid_units = ["celsius", "fahrenheit", "kelvin"]
        if units not in valid_units:
            units = "celsius"

        # API units mapping
        api_units = "metric" if units == "celsius" else "imperial" if units == "fahrenheit" else "standard"

        # Make API request
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY,
            "units": api_units
        }

        response = await http_client.get(url, params=params, timeout=API_TIMEOUT)

        if response.status_code == 401:
            return json.dumps({
                "error": "Invalid API key",
                "message": "The provided OpenWeatherMap API key is invalid",
                "status": "error"
            })
        elif response.status_code == 429:
            return json.dumps({
                "error": "Rate limit exceeded",
                "message": "API rate limit exceeded. Please try again later.",
                "status": "error"
            })

        response.raise_for_status()
        data = response.json()

        # Convert temperature if needed
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        if units == "kelvin" and api_units != "standard":
            if api_units == "metric":
                temp = temp + 273.15
                feels_like = feels_like + 273.15
            else:  # imperial
                temp = (temp - 32) * 5/9 + 273.15
                feels_like = (feels_like - 32) * 5/9 + 273.15

        # Format response
        result = {
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": round(temp, 1),
            "feels_like": round(feels_like, 1),
            "units": units,
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"].get("speed", 0),
            "wind_direction": data["wind"].get("deg", 0),
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S"),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S"),
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }

        return json.dumps(result, indent=2)

    except httpx.TimeoutException:
        return json.dumps({
            "error": "Request timeout",
            "message": "Weather API request timed out. Please try again.",
            "status": "error"
        })
    except Exception as e:
        return json.dumps({
            "error": "Unexpected error",
            "message": str(e),
            "status": "error"
        })

@mcp.tool()
async def get_weather_summary(city: str) -> str:
    """
    Get a concise weather summary with motivational message.

    Args:
        city: City name (required)

    Returns:
        JSON string with concise weather summary
    """
    try:
        # Get full weather data
        weather_data = await get_current_weather(city)
        data = json.loads(weather_data)

        if data.get("status") == "error":
            return weather_data

        # Create motivational message based on weather
        description = data["description"].lower()
        temp = data["temperature"]

        if "sun" in description or "clear" in description:
            motivation = "☀️ Perfect day to shine bright and achieve your goals!"
        elif "rain" in description:
            motivation = "🌧️ Let the rain wash away yesterday's worries - fresh start ahead!"
        elif "cloud" in description:
            motivation = "☁️ Even cloudy skies can't dim your inner light!"
        elif "snow" in description:
            motivation = "❄️ Like snowflakes, you're unique and beautiful!"
        else:
            motivation = "🌟 Every weather brings new opportunities!"

        if temp > 25:
            motivation += " Stay hydrated and keep cool! 💧"
        elif temp < 5:
            motivation += " Bundle up and stay warm! 🧥"

        summary = {
            "location": f"{data['city']}, {data['country']}",
            "temperature": f"{data['temperature']}°{data['units'][0].upper()}",
            "condition": data["description"],
            "summary": f"It's {data['temperature']}° with {data['description'].lower()} in {data['city']}",
            "motivation": motivation,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }

        return json.dumps(summary, indent=2)

    except Exception as e:
        return json.dumps({
            "error": "Summary generation failed",
            "message": str(e),
            "status": "error"
        })

@mcp.tool()
async def check_api_status() -> str:
    """
    Check OpenWeatherMap API connectivity and configuration.

    Returns:
        JSON string with API status and troubleshooting information
    """
    try:
        if not API_KEY:
            return json.dumps({
                "api_status": "not_configured",
                "message": "API key not set",
                "configuration": {
                    "api_key_set": False,
                    "default_units": DEFAULT_UNITS,
                    "timeout": API_TIMEOUT
                },
                "troubleshooting": [
                    "Set OPENWEATHER_API_KEY environment variable",
                    "Get free API key from https://openweathermap.org/api",
                    "Verify API key is active (may take up to 10 minutes after signup)"
                ],
                "status": "error"
            })

        # Test API with London
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": "London,GB",
            "appid": API_KEY,
            "units": "metric"
        }

        response = await http_client.get(url, params=params, timeout=API_TIMEOUT)

        if response.status_code == 200:
            return json.dumps({
                "api_status": "operational",
                "message": "API is working correctly",
                "configuration": {
                    "api_key_set": True,
                    "api_key_valid": True,
                    "default_units": DEFAULT_UNITS,
                    "timeout": API_TIMEOUT,
                    "provider": "OpenWeatherMap",
                    "version": "2.5"
                },
                "test_result": "Successfully retrieved weather for London",
                "supported_features": [
                    "Current weather by city name",
                    "Current weather by coordinates",
                    "Temperature unit conversion",
                    "Weather summaries with motivation"
                ],
                "status": "success"
            })
        elif response.status_code == 401:
            return json.dumps({
                "api_status": "invalid_key",
                "message": "API key is invalid",
                "configuration": {
                    "api_key_set": True,
                    "api_key_valid": False,
                    "default_units": DEFAULT_UNITS,
                    "timeout": API_TIMEOUT
                },
                "troubleshooting": [
                    "Verify API key is correct",
                    "Check if API key is activated (may take up to 10 minutes)",
                    "Ensure you're using the correct API key from your OpenWeatherMap account"
                ],
                "status": "error"
            })
        elif response.status_code == 429:
            return json.dumps({
                "api_status": "rate_limited",
                "message": "API rate limit exceeded",
                "configuration": {
                    "api_key_set": True,
                    "api_key_valid": True,
                    "default_units": DEFAULT_UNITS,
                    "timeout": API_TIMEOUT
                },
                "troubleshooting": [
                    "Wait before making more requests",
                    "Consider upgrading to a paid plan for higher limits",
                    "Free tier allows 60 calls/minute, 1,000,000 calls/month"
                ],
                "status": "warning"
            })
        else:
            return json.dumps({
                "api_status": "error",
                "message": f"API returned status code {response.status_code}",
                "configuration": {
                    "api_key_set": True,
                    "default_units": DEFAULT_UNITS,
                    "timeout": API_TIMEOUT
                },
                "troubleshooting": [
                    "Check OpenWeatherMap service status",
                    "Verify internet connectivity",
                    "Try again in a few minutes"
                ],
                "status": "error"
            })

    except httpx.TimeoutException:
        return json.dumps({
            "api_status": "timeout",
            "message": "API request timed out",
            "configuration": {
                "api_key_set": bool(API_KEY),
                "default_units": DEFAULT_UNITS,
                "timeout": API_TIMEOUT
            },
            "troubleshooting": [
                "Check internet connectivity",
                "Increase timeout value",
                "Try again later"
            ],
            "status": "error"
        })
    except Exception as e:
        return json.dumps({
            "api_status": "unknown_error",
            "message": str(e),
            "configuration": {
                "api_key_set": bool(API_KEY),
                "default_units": DEFAULT_UNITS,
                "timeout": API_TIMEOUT
            },
            "troubleshooting": [
                "Check error message above",
                "Verify all dependencies are installed",
                "Contact support if issue persists"
            ],
            "status": "error"
        })

@mcp.resource("config://weather-api")
async def get_weather_config() -> str:
    """
    Get weather API configuration and setup information.
    """
    config = {
        "api_provider": "OpenWeatherMap",
        "api_version": "2.5",
        "base_url": "https://api.openweathermap.org/data/2.5/weather",
        "documentation": "https://openweathermap.org/api",
        "features": {
            "current_weather": "Get current weather by city name or coordinates",
            "temperature_units": "Support for Celsius, Fahrenheit, and Kelvin",
            "weather_summary": "Concise summaries with motivational messages",
            "api_status": "Check API connectivity and troubleshoot issues"
        },
        "configuration": {
            "required_env_vars": ["OPENWEATHER_API_KEY"],
            "optional_env_vars": {
                "DEFAULT_UNITS": "celsius|fahrenheit|kelvin (default: celsius)",
                "WEATHER_API_TIMEOUT": "timeout in seconds (default: 10)"
            }
        },
        "setup_instructions": [
            "1. Sign up at https://openweathermap.org/api",
            "2. Get your free API key from the dashboard",
            "3. Set OPENWEATHER_API_KEY environment variable",
            "4. API key activation may take up to 10 minutes",
            "5. Test with check_api_status tool"
        ],
        "rate_limits": {
            "free_tier": "60 calls/minute, 1,000,000 calls/month",
            "paid_tiers": "Higher limits available"
        },
        "supported_cities": "All major cities worldwide with ISO country codes"
    }

    return json.dumps(config, indent=2)

@mcp.resource("data://supported-cities")
async def get_supported_cities() -> str:
    """
    Get list of popular cities for testing weather API.
    """
    cities = {
        "popular_cities": [
            "London,GB",
            "New York,US",
            "Tokyo,JP",
            "Paris,FR",
            "Sydney,AU",
            "Berlin,DE",
            "Toronto,CA",
            "Mumbai,IN",
            "São Paulo,BR",
            "Moscow,RU",
            "Beijing,CN",
            "Cairo,EG",
            "Lagos,NG",
            "Mexico City,MX",
            "Buenos Aires,AR"
        ],
        "usage_examples": {
            "by_city": {
                "description": "Get weather by city name",
                "examples": [
                    "get_current_weather('London')",
                    "get_current_weather('New York', 'US')",
                    "get_current_weather('Tokyo', 'JP', 'fahrenheit')"
                ]
            },
            "by_coordinates": {
                "description": "Get weather by latitude and longitude",
                "examples": [
                    "get_weather_by_coordinates(51.5074, -0.1278)",  # London
                    "get_weather_by_coordinates(40.7128, -74.0060, 'fahrenheit')",  # NYC
                    "get_weather_by_coordinates(35.6762, 139.6503, 'kelvin')"  # Tokyo
                ]
            },
            "summary": {
                "description": "Get motivational weather summary",
                "examples": [
                    "get_weather_summary('Paris')",
                    "get_weather_summary('Sydney')"
                ]
            }
        },
        "country_codes": {
            "note": "Use ISO 3166-1 alpha-2 country codes",
            "examples": {
                "GB": "United Kingdom",
                "US": "United States",
                "JP": "Japan",
                "FR": "France",
                "DE": "Germany",
                "CA": "Canada",
                "AU": "Australia"
            }
        },
        "tips": [
            "Include country code for better accuracy",
            "Use English city names",
            "Check spelling if city not found",
            "Some cities may have multiple matches - use country code to specify"
        ]
    }

    return json.dumps(cities, indent=2)

# Server startup and lifecycle management
async def setup_http_client():
    """Initialize HTTP client with proper configuration."""
    global http_client
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(API_TIMEOUT),
        headers={"User-Agent": "WeatherMCP/1.0"}
    )

async def cleanup_http_client():
    """Clean up HTTP client resources."""
    global http_client
    if http_client:
        await http_client.aclose()
        http_client = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    _ = signum, frame  # Acknowledge parameters
    print("Shutting down WeatherMCP server...")
    sys.exit(0)

async def initialize_server():
    """Initialize the server components."""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize HTTP client
    await setup_http_client()

if __name__ == "__main__":
    # Initialize server components
    asyncio.run(initialize_server())

    # Run the MCP server (this handles its own event loop)
    mcp.run()

# Test cases:
# get_current_weather("London", "GB", "celsius")
# get_weather_by_coordinates(40.7128, -74.0060, "fahrenheit")
# get_weather_summary("Tokyo")
# check_api_status()
