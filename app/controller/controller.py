from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List

from app.schema.validation import Comment, Inputs, ErrorResponse
from app.log.app_logger import logger
from app.views.view import get_comments


router = APIRouter()

@router.get("/api/v1/subfeddit_catagory", tags=["Comments by Name"], 
    summary="Get Comments with sentiment score",
    description="Retrieve comments from subfeddit id by providing name of subfeddit.  \n "
                "Latest Comments will be provided with sentiment value .  \n"
                "Data can be sort by polarity score if **sort_by_polarity** is **True**.  \n" 
                "Data Can be Filter by start date, end date and must be passed as **DD-MM-YYYY** format",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "comment_id": "1",
						"text": "It looks great!",
                        "polarity_score": "0.54",
						"sentiment": "Positive"
                    }
                }
            }
        },404: {"model": ErrorResponse}})
def comments_score(request: Request, payload: Inputs = Depends(), ):

    logger.info(f"Subfeddit analysis started for subfeddit {payload.subfeddit_name}")


    ip = request.client.host
    logger.info(f"Request recieved from {ip}")
    response = get_comments(payload)
    if not response:
        return {"message":"No Records Found"}
    return response
    
    