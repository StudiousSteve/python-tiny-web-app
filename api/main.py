import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Any

app = FastAPI()
templates = Jinja2Templates(directory="templates")

NWS_API_URL = "https://api.weather.gov/gridpoints/MPX/107,65/forecast"

async def get_weather()->list[Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(NWS_API_URL)
        responses  = []
        if response.status_code == 200:
            responses: list[Any] = response.json().get("properties", {}).get("periods", [])
        return responses

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    weather_data = await get_weather()
    return templates.TemplateResponse("index.html", {"request": request, "weather": weather_data})

@app.get("/click", response_class=HTMLResponse)
async def click(request: Request):
    unit = request.query_params.get("unit", "fahrenheit")  # Default to F
    print(f"Received unit: {unit}") 

    weather_data = await get_weather()
    content = """
    <div class="mt-4 bg-gray-800 p-4 rounded-lg shadow-lg relative flex flex-col items-center">
        <div class="flex justify-end w-full">
            <button 
                class="w-5 h-5 flex items-center justify-center"
                onclick="document.getElementById('forecast-container').innerHTML = ''"
                >
                    <svg class="w-4 h-4 text-gray-400 hover:text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M6 6l8 8m0-8l-8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
            </button>

        </div>
    <ul class='divide-y divide-gray-700'>
    """

    for period in weather_data[:5]:
        content += f"""<li class='py-2'><strong>{period['name']}</strong>: 
                      {period['temperature']}°F, 
                      <span class='text-blue-400'>{period['shortForecast']}</span></li>"""
    content += "</ul>"
    return content  # Returns only the forecast list, keeping styling intact
