from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import operator

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Allowed operators
ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda a, b: a / b if b != 0 else "Cannot divide by zero"
}


@app.get("/", response_class=HTMLResponse)
async def get_calculator(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/calculate")
async def calculate(expr: str):
    try:
        # Very simple parser (split by space)
        parts = expr.split()
        if len(parts) != 3:
            return JSONResponse({"result": "Invalid expression"})

        num1 = float(parts[0])
        op = parts[1]
        num2 = float(parts[2])

        if op in ops:
            result = ops[op](num1, num2)
        else:
            result = "Invalid operator"

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"result": f"Error: {str(e)}"})
