# services/api-server/app/repositories/conversation_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, or_, desc
from typing import List, Optional, Dict, Any
from app.models import Conversation, Message
from app.schemas import ConversationResponse, MessageResponse
import logging
from app.utils.idgen import generate_ulid

logger = logging.getLogger(__name__)

async def create_conversation(session: AsyncSession, conversation_id: str, title: str, user_id: str) -> Conversation:
    """Create a new conversation for a specific user"""
    conversation = Conversation(
        id=conversation_id,
        user_id=user_id,
        title=title
    )
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation

async def get_conversation(session: AsyncSession, conversation_id: str, user_id: Optional[str] = None) -> Optional[ConversationResponse]:
    """Get conversation by ID, with optional user filtering"""
    query = select(Conversation).where(Conversation.id == conversation_id)

    # If user_id is provided, ensure the conversation belongs to this user
    if user_id:
        query = query.where(Conversation.user_id == user_id)

    result = await session.execute(query)
    conversation = result.scalar_one_or_none()

    if conversation:
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
    return None

async def get_conversations(session: AsyncSession, user_id: str, skip: int = 0, limit: int = 50) -> List[ConversationResponse]:
    """Get paginated list of conversations for a specific user"""
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()

    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            user_id=conv.user_id,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]

async def get_all_conversations(session: AsyncSession, skip: int = 0, limit: int = 50) -> List[ConversationResponse]:
    """Get all conversations (admin only) - no user filtering"""
    result = await session.execute(
        select(Conversation)
        .offset(skip)
        .limit(limit)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()

    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            user_id=conv.user_id,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]

async def add_message(session: AsyncSession, conversation_id: str, role: str, content: str, metadata: dict = None) -> Message:
    """Add message to conversation"""
    message = Message(
        conversation_id=conversation_id,
        #role=role,
        is_user_message=(role == "user"), # Changed from 'role' to 'is_user_message'
        content=content,
        # metadata=metadata or {}
        message_metadata=metadata or {}    # Changed from 'metadata' to 'message_metadata'
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message

async def get_messages(session: AsyncSession, conversation_id: str, user_id: Optional[str] = None) -> List[MessageResponse]:
    """Get all messages for a conversation, with optional user ownership check"""
    # First verify the conversation exists and belongs to user if user_id provided
    if user_id:
        conv_query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conv_result = await session.execute(conv_query)
        conversation = conv_result.scalar_one_or_none()
        if not conversation:
            return []  # Conversation doesn't exist or doesn't belong to user

    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    messages = result.scalars().all()

    return [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at
        )
        for msg in messages
    ]

async def delete_conversation(session: AsyncSession, conversation_id: str, user_id: Optional[str] = None) -> bool:
    """Delete conversation and its messages, with optional user ownership check"""
    try:
        # Build query with optional user filter
        if user_id:
            # First verify the conversation belongs to the user
            conv_query = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conv_result = await session.execute(conv_query)
            conversation = conv_result.scalar_one_or_none()
            if not conversation:
                return False  # Conversation doesn't exist or doesn't belong to user

        # Delete messages first
        await session.execute(
            delete(Message).where(Message.conversation_id == conversation_id)
        )

        # Delete conversation
        result = await session.execute(
            delete(Conversation).where(Conversation.id == conversation_id)
        )
        await session.commit()

        return result.rowcount > 0

    except Exception as e:
        await session.rollback()
        raise e

async def update_conversation_title(session: AsyncSession, conversation_id: str, new_title: str, user_id: Optional[str] = None) -> bool:
    """Update conversation title, with optional user ownership check"""
    try:
        query = update(Conversation).where(Conversation.id == conversation_id)

        # Add user filter if provided
        if user_id:
            query = query.where(Conversation.user_id == user_id)

        query = query.values(title=new_title)

        result = await session.execute(query)
        await session.commit()

        return result.rowcount > 0

    except Exception as e:
        await session.rollback()
        raise e

async def get_conversation_count(session: AsyncSession, user_id: Optional[str] = None) -> int:
    """Get total conversation count, with optional user filtering"""
    query = select(Conversation)

    if user_id:
        query = query.where(Conversation.user_id == user_id)

    result = await session.execute(query)
    conversations = result.scalars().all()

    return len(conversations)

async def search_conversations(session: AsyncSession, query: str, user_id: str, skip: int = 0, limit: int = 50) -> List[ConversationResponse]:
    """Search conversations by title for a specific user"""
    result = await session.execute(
        select(Conversation)
        .where(
            Conversation.user_id == user_id,
            or_(
                Conversation.title.ilike(f"%{query}%"),
                Conversation.id.ilike(f"%{query}%")
            )
        )
        .offset(skip)
        .limit(limit)
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()

    return [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
            user_id=conv.user_id,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        )
        for conv in conversations
    ]
