from utils.app import app as ec_app
from utils.app import loader, chunker
from fastapi import APIRouter, Query, responses
from pydantic import BaseModel

router = APIRouter()

class SourceModel(BaseModel):
    source: str


class QuestionModel(BaseModel):
    question: str
    session_id: str

@router.post("/api/v1/add")
async def add_source(source_model: SourceModel):
    """
    Adds a new source to the Embedchain app.
    Expects a JSON with a "source" key.
    """
    source = source_model.source
    try:
        ec_app.add(source, data_type="slack", loader=loader, chunker=chunker)
        return {"message": f"Source '{source}' added successfully."}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
        return {"message": response}


@router.get("/api/v1/chat")
async def handle_chat(query: str, session_id: str = Query(None)):
    """
    Handles a chat request to the Embedchain app.
    Accepts 'query' and 'session_id' as query parameters.
    """
    try:
        response = ec_app.chat(query, session_id=session_id)
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
    return {"response": response}

@router.get("/api/v1/channels")
async def handle_channels(slack_user_token: str):
    """
    Handles a channel list request to the Embedchain app.
    Accepts 'user_token' as a query parameter.
    """
    try:
        response = loader.get_channels(slack_user_token)
        return {"message": response}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"
        return {"message": response}

@router.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
