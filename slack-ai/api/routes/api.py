import os

from fastapi import APIRouter, Query, responses
from pydantic import BaseModel

from utils.app import chunker, ec_app, loader

router = APIRouter()


class SourceModel(BaseModel):
    channel: str


class QuestionModel(BaseModel):
    question: str
    session_id: str


@router.post("/api/v1/add")
async def add_channel_data(source_model: SourceModel):
    """
    Adds a new source to the Embedchain app.
    Expects a JSON with a "channel" key.
    """
    channel = source_model.channel.replace("#", "").strip()
    try:
        ec_app.add(f"in:{channel}", data_type="slack", loader=loader, chunker=chunker)
        return {"message": f"Data for '{channel}' added successfully."}
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
        answer, metadata = ec_app.chat(query, session_id=session_id, citations=True)
        citations = []
        for i in metadata:
            citations.append(i[1]["url"])
        response = {"answer": answer, "citations": list(set(citations))}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
    return {"response": response}


@router.get("/api/v1/channels")
async def get_channels():
    """
    Handles a channel list request to the Embedchain app.
    Accepts 'user_token' as a query parameter.
    """
    try:
        # List all channels in slack: https://api.slack.com/methods/conversations.list
        response = loader.get_channels(os.environ["SLACK_USER_TOKEN"])
        return {"message": response}
    except Exception as e:
        response = f"An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
        return {"message": response}


@router.get("/api/v1/reset")
async def reset_app():
    """
    Resets the Embedchain app.
    """
    try:
        ec_app.reset()
        return {"message": "Embedchain app reset successfully."}
    except Exception:
        response = "An error occurred: Error message: {str(e)}. Contact Embedchain founders on Slack: https://embedchain.com/slack or Discord: https://embedchain.com/discord"  # noqa:E501
        return {"message": response}


@router.get("/")
async def root():
    return responses.RedirectResponse(url="/docs")
