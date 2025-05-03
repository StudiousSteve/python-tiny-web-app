from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount(path="/back-end/static", app=StaticFiles(directory="back-end/static"), name="static")

@app.get(path="/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
	response = templates.TemplateResponse("home.html", {"request": request})
	return HTMLResponse(content=response.body)


@app.get(path="/data")
def get_data() -> HTMLResponse:
	return HTMLResponse("<p>Fetched Data!</p>")
