import { Agent } from "@mastra/core/agent";
import { MCPClient } from "@mastra/mcp";
import { openai } from "@ai-sdk/openai";

const apiKey = process.env.SMITHERY_API_KEY as string;
const profileKey = process.env.SMITHERY_PROFILE_KEY as string;

// Initialize MCP Client with your weather MCP server
const mcp = new MCPClient({
    servers: {
        "mcp": {
            command: "npx",
            args: [
                "-y",
                "@smithery/cli@latest",
                "run",
                "@Arliiii/mcp",
                "--key",
                apiKey,
                "--profile",
                profileKey,
            ],
            timeout: 30000, // 30 second timeout
        },
    },
});

// Create agent with access to MCP tools
const weatherAgent = new Agent({
    name: "Weather Assistant",
    instructions: `You are a helpful weather assistant that can provide accurate weather information for any location.
  
  Your capabilities include:
  - Getting current weather conditions
  - Providing weather forecasts
  - Answering weather-related questions
  - Helping users plan activities based on weather conditions
  
  Always use the available weather tools to get the most current and accurate information.
  When providing weather information, be specific about the location and include relevant details like temperature, conditions, humidity, and wind if available.`,
    model: openai("gpt-3.5-turbo"),
    tools: await mcp.getTools(), // Get all tools from MCP servers
});

export { weatherAgent };