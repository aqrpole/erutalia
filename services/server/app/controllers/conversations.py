from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas import ConversationCreate, ConversationResponse, MessageResponse
from app.repositories.conversation_repository import (
    create_conversation,
    get_conversation,
    get_conversations
)
from app.core.auth import get_current_active_user, require_user

router = APIRouter()

@router.get("/conversations")
async def get_conversations():
    """Get all conversations for the current user"""
    return {"message": "Get conversations endpoint"}

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: dict = Depends(require_user)
):
    """Get specific conversation (user can only access their own)"""
    user_id = current_user.get("user_id")
    conversation = await get_conversation(conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if user owns this conversation
    if conversation.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return conversation

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(require_user)
):
    """Get list of conversations for current user"""
    user_id = current_user.get("user_id")
    return await get_conversations(user_id, skip, limit)

@router.post("/conversations")
async def create_conversation():
    """Create a new conversation"""
    return {"message": "Create conversation endpoint"}

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    current_user: dict = Depends(require_user)
):
    """Delete a conversation (user can only delete their own)"""
    user_id = current_user.get("user_id")
    conversation = await get_conversation(conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if user owns this conversation
    if conversation.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    success = await conversation_repo.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted"}
