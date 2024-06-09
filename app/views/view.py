from datetime import datetime
from fastapi import HTTPException
import requests
import multiprocessing

from app.config.configs import settings
from app.log.app_logger import logger
from app.views.sentiment_pred import sentiment_analysis

def form_url(endpoint,param: dict=None):

    ip = settings.get("feddit_host")
    port = settings.get("feddit_port")
    base = settings.get("feddit_base_url")

    params = []
    if param:
        for key, val in param.items():
            res = ""
            res = f"{key}={val}"
            params.append(res)

        query = "&".join(params)
        url = f"http://{ip}:{port}/{base}/{endpoint}/?{query}"

    else:
        url = f"http://{ip}:{port}/{base}/{endpoint}"

    return url

def fetch_data_chunk(id: int, skip: int, limit: int):

    logger.info(f"forming all comments url")
    endpoint = settings.get("feddit_comment")
    param = {"subfeddit_id": id, "skip": skip, "limit":limit}
    url = form_url(endpoint,param) 
    response = requests.get(url)
    if response.status_code != 200:

        raise HTTPException(status_code=response.status_code ,detail=f"Error fetching data from API {url} with error : {response.text}")
    
    return response.json()

def get_sentiment_value(data: list, start_date: str = None, end_date: str = None, sort_val: bool = False):
    
    try:
        res = None
        if not (start_date and end_date):
            data = data[0]["comments"]
            res = sentiment_analysis(data)

        else:
            start_date = int(float(start_date))
            end_date = int(float(end_date))
            filtered_data = []

            for subfeddit in data:
            
                filtered_comments = [comment for comment in subfeddit['comments'] if start_date <= comment['created_at'] <= end_date]

                if filtered_comments:
                    filtered_data.extend(filtered_comments)

            if filtered_data:
                res = sentiment_analysis(filtered_data)
        
        if sort_val and res:
            logger.info(f"Sorting results as per polarity score")
            res = sorted(res, key=lambda x: x['polarity_score'])
    
    except Exception as ex:
        logger.error(f"Error occured while getting sentiment score with error {ex}")
        raise HTTPException(status_code=500, detail=f"Error occured while getting sentiment score with error {ex}")


    return res


def get_comments(payload):
    logger.info(f"Getting comments by subfeddit name {payload.subfeddit_name}")

    try:
        data = payload.dict()
        name = payload.subfeddit_name
        id = None
        start_date = payload.start_date
        end_date = payload.end_date
        sort_value = payload.sort_by_polarity

        logger.info(f"forming all subfeddit url")

        endpoint = settings.get("feddit_all")
        param = {"skip": 0, "limit":10}

        url = form_url(endpoint,param)

        logger.info(f"Calling all subfeddit url")
        
        result = requests.get(url).json()

        for val in result["subfeddits"]:
            if val["title"] == name:
                id = val["id"]

        if not id:
            raise HTTPException(status_code=404, detail=f"Subfeddit name {name} not found ,please give valid name")
        

        logger.info(f"Getting all comments by subfeddit id {id}")

        data = []
        
        if not (start_date and end_date):
            chunk_size = 25
            skip_values = range(0, 100, chunk_size)  
        
        else:
            chunk_size = 3000
            skip_values = range(0, 30000, chunk_size)
            
        pool = multiprocessing.Pool()
        results = [pool.apply_async(fetch_data_chunk, (id, skip, chunk_size)) for skip in skip_values]

        pool.close()
        pool.join()

        
        for result in results:
            data.append(result.get())

        response = get_sentiment_value(data, start_date, end_date, sort_value)
        

    except Exception as e:
        logger.error(f"Error fetching comments: {e}")
        return {"error msg": f"Error fetching comments: {e}"}
    
    return response
