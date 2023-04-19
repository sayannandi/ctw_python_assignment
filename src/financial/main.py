from fastapi import FastAPI, Request

from src.financial.controller import get_financial_data, get_statistics


app = FastAPI()


def index():
    return {'success': True}


@app.get("/api/financial_data")
async def financial_data_handler(request: Request):
    return get_financial_data(request.query_params)


@app.get("/api/statistics")
async def financial_data_handler(request: Request):
    return get_statistics(request.query_params)
