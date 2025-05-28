#!/usr/bin/env python3
"""
Test script for WeatherMCP server.
Run this to verify your weather MCP server is working correctly.
"""

import asyncio
import json
import os
from fastmcp import Client
import weather_server

async def test_weather_mcp():
    """Test all weather MCP tools and resources."""
    print("🌤️ Testing WeatherMCP Server")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("❌ OPENWEATHER_API_KEY environment variable not set!")
        print("Please set your API key and try again.")
        return
    
    print(f"✅ API key is set: {api_key[:8]}...")
    print()
    
    # Create client
    client = Client(weather_server.mcp)
    
    async with client:
        # Test 1: Check API Status
        print("🔍 Test 1: Checking API Status")
        try:
            result = await client.call_tool("check_api_status", {})
            data = json.loads(result[0].text)
            print(f"Status: {data.get('api_status', 'unknown')}")
            print(f"Message: {data.get('message', 'No message')}")
            if data.get('status') == 'success':
                print("✅ API is working correctly!")
            else:
                print("❌ API check failed!")
                print("Troubleshooting tips:")
                for tip in data.get('troubleshooting', []):
                    print(f"  - {tip}")
        except Exception as e:
            print(f"❌ API status check failed: {e}")
        
        print()
        
        # Test 2: Get weather for London
        print("🌍 Test 2: Getting weather for London, GB")
        try:
            result = await client.call_tool("get_current_weather", {
                "city": "London",
                "country_code": "GB",
                "units": "celsius"
            })
            data = json.loads(result[0].text)
            if data.get('status') == 'success':
                print(f"✅ {data['city']}, {data['country']}: {data['temperature']}°C")
                print(f"   Condition: {data['description']}")
                print(f"   Feels like: {data['feels_like']}°C")
            else:
                print(f"❌ Failed: {data.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Weather request failed: {e}")
        
        print()
        
        # Test 3: Get weather by coordinates (New York)
        print("📍 Test 3: Getting weather by coordinates (New York)")
        try:
            result = await client.call_tool("get_weather_by_coordinates", {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "units": "fahrenheit"
            })
            data = json.loads(result[0].text)
            if data.get('status') == 'success':
                print(f"✅ {data['city']}, {data['country']}: {data['temperature']}°F")
                print(f"   Coordinates: {data['coordinates']['latitude']}, {data['coordinates']['longitude']}")
            else:
                print(f"❌ Failed: {data.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Coordinates request failed: {e}")
        
        print()
        
        # Test 4: Get weather summary
        print("📝 Test 4: Getting weather summary for Tokyo")
        try:
            result = await client.call_tool("get_weather_summary", {
                "city": "Tokyo"
            })
            data = json.loads(result[0].text)
            if data.get('status') == 'success':
                print(f"✅ {data['location']}: {data['temperature']}")
                print(f"   Summary: {data['summary']}")
                print(f"   Motivation: {data['motivation']}")
            else:
                print(f"❌ Failed: {data.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Summary request failed: {e}")
        
        print()
        
        # Test 5: Get configuration resource
        print("⚙️ Test 5: Getting configuration resource")
        try:
            result = await client.read_resource("config://weather-api")
            data = json.loads(result[0].text)
            print(f"✅ API Provider: {data['api_provider']}")
            print(f"   Version: {data['api_version']}")
            print(f"   Features: {len(data['features'])} available")
        except Exception as e:
            print(f"❌ Config resource failed: {e}")
        
        print()
        
        # Test 6: Get supported cities resource
        print("🏙️ Test 6: Getting supported cities resource")
        try:
            result = await client.read_resource("data://supported-cities")
            data = json.loads(result[0].text)
            print(f"✅ Popular cities: {len(data['popular_cities'])} available")
            print(f"   Examples: {', '.join(data['popular_cities'][:5])}...")
        except Exception as e:
            print(f"❌ Cities resource failed: {e}")
    
    print()
    print("🎉 Testing completed!")
    print("If all tests passed, your WeatherMCP server is ready for deployment!")

if __name__ == "__main__":
    asyncio.run(test_weather_mcp())
