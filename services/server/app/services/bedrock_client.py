# services/server/app/services/bedrock_client.py
import boto3
import json
import os
import logging
import re
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

def clean_response(text):
    """Remove all reasoning, thinking, and explanatory text from the response"""
    if not text:
        return ""
    
    # Remove reasoning tags and content between them
    text = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL)
    
    # Remove common reasoning phrases and their content
    reasoning_patterns = [
        r'<thinking>.*?</thinking>',
        r'<reasoning>.*?</reasoning>',
        r'We have a user asking.*?So we can answer',
        r'The user asks.*?According to policy',
        r'We need to answer.*?directly',
        r'This is a.*?question',
        r'According to.*?policy',
        r'Let me.*?think',
        r'I should.*?answer',
        r'First.*?then',
        r'Looking at.*?question',
    ]
    
    for pattern in reasoning_patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove multiple spaces and trim
    text = re.sub(r'\s+', ' ', text).strip()
    
    # If there's still explanatory text, try to extract just the answer part
    direct_patterns = [
        r'is\s+([^.!?]+)[.!?]',  # "is Paris" or "is Paris."
        r'are\s+([^.!?]+)[.!?]', # "are 8 planets"
        r':\s*([^.!?]+)[.!?]',   # "Answer: Paris"
        r'-\s*([^.!?]+)[.!?]',   # "- Paris"
    ]
    
    for pattern in direct_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    # If we still have a long answer, take the first sentence
    sentences = re.split(r'[.!?]', text)
    if sentences:
        first_sentence = sentences[0].strip()
        # If first sentence still contains reasoning words, try second
        reasoning_words = ['user', 'asks', 'question', 'according', 'policy', 'thinking', 'reasoning']
        if any(word in first_sentence.lower() for word in reasoning_words) and len(sentences) > 1:
            return sentences[1].strip()
        return first_sentence
    
    return text

async def generate_bedrock_response(prompt: str, context: List[Dict[str, Any]] = None) -> str:
    """Generate response using OpenAI models through AWS Bedrock with Qdrant context"""
    try:
        logger.info(f"Generating Bedrock response for prompt: {prompt}")
        
        # Create Bedrock client
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.BEDROCK_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        # Build the enhanced prompt with Qdrant context
        if context and len(context) > 0:
            # Extract text from Qdrant search results
            context_texts = []
            for doc in context:
                content = doc.get("text", doc.get("content", ""))
                if content:
                    context_texts.append(f"- {content}")
            
            context_text = "\n".join(context_texts)
            
            enhanced_prompt = f"""Based on the following context information:

{context_text}

User Question: {prompt}

Please provide a direct answer based only on the context provided. If the context doesn't contain relevant information to answer the question, simply say "I don't have enough information to answer this question based on the available documents." Do not include any reasoning, thinking, or explanations."""
        else:
            # No context from Qdrant
            enhanced_prompt = f"""User Question: {prompt}

Please provide a direct answer. If you cannot answer based on your knowledge, simply say "I don't have enough information to answer this question." Do not include any reasoning, thinking, or explanations."""

        # Prepare the request for OpenAI model
        native_request = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Provide direct, concise answers without any reasoning, thinking, or explanation. Just answer the question directly based on the provided context. If the context doesn't contain the answer, say you don't know."
                },
                {
                    "role": "user", 
                    "content": enhanced_prompt
                }
            ],
            "max_completion_tokens": 500,
            "temperature": 0.3,  # Lower temperature for more consistent answers
            "top_p": 0.9
        }

        logger.info(f"Sending request to Bedrock model: {settings.BEDROCK_MODEL_ID}")
        
        # Make the InvokeModel request
        response = client.invoke_model(
            modelId=settings.BEDROCK_MODEL_ID,
            body=json.dumps(native_request)
        )

        # Parse the response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        
        # Extract the assistant's message content
        if 'choices' in response_body and len(response_body['choices']) > 0:
            answer = response_body['choices'][0]['message']['content']
            
            # Clean the response aggressively to remove reasoning
            clean_answer = clean_response(answer)
            
            logger.info(f"Bedrock response generated successfully")
            logger.info(f"Original answer: {answer}")
            logger.info(f"Cleaned answer: {clean_answer}")
            
            return clean_answer
        else:
            logger.error("No answer found in Bedrock response")
            return "I apologize, but I couldn't generate a response at this time."

    except Exception as e:
        logger.error(f"Bedrock API error: {str(e)}")
        raise

async def health_check() -> bool:
    """Check if Bedrock service is accessible"""
    try:
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.BEDROCK_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        
        # Try a simple list models call as health check
        client.list_foundation_models(MaxResults=1)
        logger.info("✅ Bedrock health check passed")
        return True
    except Exception as e:
        logger.error(f"❌ Bedrock health check failed: {e}")
        return False