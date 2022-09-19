from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()  #整個主程式
templates = Jinja2Templates("templates")



@app.get("/")   #修飾符，用來修飾整個get index 的function  #router -> assign path
def get_index():  # handler -> logic layer
    #json
    resp = {    #這個resp是變數 可以隨意換
        "index" : "hi"
    }  # provided response for users

    return resp  # response  #這個resp是變數 可以隨意換


@app.get("/page", response_class=HTMLResponse)
def get_page(request: Request):
    context = {
        "request": request,
        "ids" : [1, 2, 3, 4,]
    }
    return templates.TemplateResponse("/index.html", context=context)
