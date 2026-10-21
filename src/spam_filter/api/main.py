
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from spam_filter.api.schemas import EmailRequestValidation
from spam_filter.modeling.predict import run_prediction_pipeline, CLASSES

app = FastAPI()

# Serve static files like CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set the template directory
templates = Jinja2Templates(directory="static/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(name="index.html" , request=request)




@app.post("/predict")
def predict(request : EmailRequestValidation):

    subject = request.subject
    body = request.body


    result = run_prediction_pipeline( subject=subject,   body=body )

    print(result)

    return  {"label" :CLASSES[result]}


    


