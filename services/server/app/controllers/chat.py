import logging
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi import status
from app.schemas import ChatRequest, ChatResponse
from app.services.ollama_client import OllamaClient
from app.services.qdrant_client import QdrantClient
from app.core.auth import get_current_active_user, require_user
from app.repositories.conversation_repository import ConversationRepository
from app.utils.idgen import generate_ulid

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
    current_user: dict = Depends(require_user),  # Require user role
    ollama_client: OllamaClient = Depends(lambda: ollama_client),
    qdrant_client: QdrantClient = Depends(lambda: qdrant_client),
    conversation_repo: ConversationRepository = Depends()
):
    """Send a message to the LLM and get response (Authenticated)"""
    try:
        user_id = current_user.get("user_id")  # From JWT token
        
        # Get relevant context from Qdrant
        query_embedding = await ollama_client.generate_embeddings(request.message)
        relevant_context = await qdrant_client.search_similar(
            query_embedding, 
            limit=3
        )
        
        # Build context-aware prompt
        context_text = "\n".join([doc["content"] for doc in relevant_context])
        enhanced_prompt = f"""Context: {context_text}

        User Question: {request.message}

        Please answer based on the context provided."""
        
        # Get LLM response
        response = await ollama_client.generate_response(enhanced_prompt)
        
        # Create or update conversation with user_id
        if not request.conversation_id:
            conversation_id = generate_ulid()
            await conversation_repo.create_conversation(
                conversation_id, 
                request.message[:100] + "...",
                user_id=user_id  # Associate with authenticated user
            )
        else:
            conversation_id = request.conversation_id
        
        # Save messages
        message_id = generate_ulid()
        await conversation_repo.add_message(
            conversation_id, "user", request.message
        )
        await conversation_repo.add_message(
            conversation_id, "assistant", response
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            message_id=message_id,
            response=response,
            sources=relevant_context
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