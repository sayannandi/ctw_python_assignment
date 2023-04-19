import math
from src.model import FinancialData
from src.financial.validator import FinancialDataRequestSchema, StatisticsRequestSchema


def get_financial_data(params):
    err, params = _validate_and_load_params(params, FinancialDataRequestSchema())
    
    if err:
        cnt, data = 0, []
    else:
        cnt, data = FinancialData.get_financial_data(**params)

    resp = dict(
        data=data,
        pagination=_get_pagination_info(params, cnt),
        info=dict(error=err)
    )

    return resp


def get_statistics(params):
    err, params = _validate_and_load_params(params, StatisticsRequestSchema())

    if err:
        data = []
    else:
        data = FinancialData.get_statistics(**params)
    
    resp = dict(
        data=data,
        info=dict(error=err)
    )

    return resp

def _get_pagination_info(params, cnt):
    limit = params['limit']
    page = params['page']
    
    pagination_info = dict(
        count=cnt,
        page=page,
        limit=limit,
        pages=math.ceil(cnt / limit)
    )
    return pagination_info

def _validate_and_load_params(params, schema):
    err, validated_params = '', {}
    try:
        validated_params = schema.load(params)
    except Exception as ex:
        err = str(ex)

    return err, validated_params
