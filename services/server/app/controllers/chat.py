import logging
from fastapi                                  import APIRouter, Depends, HTTPException
from fastapi                                  import status, WebSocket, WebSocketDisconnect
from app.schemas                              import ChatRequest, ChatResponse
from app.services.qdrant_client               import search_similar
from app.core.auth                            import get_current_active_user, require_user
from app.utils.idgen                          import generate_ulid
#from app.services.ollama_client               import generate_response, get_session, generate_embeddings
from app.services.bedrock_client              import (generate_response,
                                                      generate_embeddings)
from app.repositories.conversation_repository import get_conversation, create_conversation, add_message
from app.core.database                        import get_db
from sqlalchemy.ext.asyncio                   import AsyncSession

router = APIRouter()  # This line is crucial
logger = logging.getLogger(__name__)

@router.get("/messages")
async def get_messages():
    return {"message": "Get messages endpoint"}

@router.post("/messages")
async def send_message():
    return {"message": "Send message endpoint"}

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict   =Depends (require_user),  # Require user role
    session: AsyncSession=Depends (get_db)
):
    """Send a message to the LLM and get response (Authenticated)"""
    try:
        # Call Ollama (functional) directly
        #response_text = await generate_response (
        #    prompt=request.prompt,
        #    context=request.context  # optional
        #)

        user_id = current_user.get ("sub")  # From JWT token
        #logger.info (f"user_id= {type (user_id)} - {user_id}")

        # Get relevant context from Qdrant
        query_embedding  = await generate_embeddings (request.message)
        try:
            relevant_context = await search_similar (
                query_embedding,
                limit=3
            )
        except Exception as e:
            logger.warning (f"Qdrant unavailable: {e}")

        # Build context-aware prompt
        context_text = "\n".join([doc["content"] for doc in relevant_context])
        enhanced_prompt = f"""Context: {context_text}

        User Question: {request.message}

        Please answer based on the context provided."""

        # Get LLM response
        response = await generate_response(enhanced_prompt)

        # Create or update conversation with user_id
        if not request.conversation_id:
            conversation_id = generate_ulid ()
            await create_conversation (
                session        =session,
                conversation_id=conversation_id,
                title          =request.message[:100] + "...",
                user_id        =user_id,  # Associate with authenticated user
            )
        else:
            conversation_id = request.conversation_id

        # Save messages
        message_id = generate_ulid ()
        await add_message(
            session        =session,
            conversation_id=conversation_id,
            role           ="user",
            content        =request.message
        )
        await add_message(
            session        =session,
            conversation_id=conversation_id,
            role           ="assistant",
            content        =response
        )

        return ChatResponse(
            conversation_id=conversation_id,
            message_id     =message_id,
            response       =response,
            sources        =relevant_context
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process chat request")

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Handle WebSocket chat messages
            await websocket.send_json({"type": "message", "content": "Response"})
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close(code=1011)
