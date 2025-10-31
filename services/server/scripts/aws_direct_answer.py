import boto3
import json
import os
import asyncio
from dotenv import load_dotenv
import re

# Load environment variables from .env one folder up
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

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
    # Look for patterns like "The capital of France is Paris" -> extract "Paris"
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

async def get_direct_answer(question):
    """Get a direct answer without reasoning"""
    try:
        print(f"🧪 Asking: {question}")

        # Load configuration from environment
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("BEDROCK_REGION", "us-east-1")
        model_id = os.getenv("BEDROCK_MODEL_ID", "openai.gpt-oss-20b-1:0")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("Missing AWS credentials in .env file")

        # Create Bedrock client
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        # Direct approach - force simple answers
        native_request = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Provide direct, concise answers without any reasoning, thinking, or explanation. Just answer the question directly."
                },
                {
                    "role": "user", 
                    "content": question
                }
            ],
            "max_completion_tokens": 150,  # Shorter to force concise answers
            "temperature": 0.5,  # Lower temperature for more deterministic answers
            "top_p": 0.9
        }

        # Make the InvokeModel request
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(native_request)
        )

        # Parse the response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        
        # Extract just the assistant's message content
        if 'choices' in response_body and len(response_body['choices']) > 0:
            answer = response_body['choices'][0]['message']['content']
            
            # Clean the response aggressively
            clean_answer = clean_response(answer)

            # Clean up the response - remove any reasoning tags
            clean_answer = answer.replace('<reasoning>', '').replace('</reasoning>', '').strip()
            
            print(f"✅ Question: {question}")
            print(f"✅ Direct Answer: {clean_answer}")
            
            return clean_answer
        else:
            print("❌ No answer found in response")
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def get_structured_answer(question):
    """Get answer in JSON format"""
    try:
        print(f"🧪 Asking with JSON format: {question}")

        # Load configuration from environment
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("BEDROCK_REGION", "us-east-1")
        model_id = os.getenv("BEDROCK_MODEL_ID", "openai.gpt-oss-20b-1:0")

        # Create Bedrock client
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        # Force JSON-like response
        native_request = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Always respond with just the direct answer in plain text. Do not include any reasoning, thinking, or explanations. Just the answer."
                },
                {
                    "role": "user", 
                    "content": f"Answer this question directly without any explanation: {question}"
                }
            ],
            "max_completion_tokens": 30,
            "temperature": 0.0,  # Minimum temperature for most deterministic output
            "top_p": 0.1
        }

        # Make the InvokeModel request
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(native_request)
        )

        # Parse the response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        
        # Extract the answer
        if 'choices' in response_body and len(response_body['choices']) > 0:
            answer = response_body['choices'][0]['message']['content']
            
            # Return clean answer
            return answer.strip()
        else:
            return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


async def batch_questions():
    """Test multiple questions"""
    questions = [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?",
        "What is 2+2?",
        "How many planets are in our solar system?"
    ]
    
    print("=== Testing Multiple Questions ===")
    
    for question in questions:
        answer = await get_direct_answer(question)
        if answer:
            print(f"Q: {question}")
            print(f"A: {answer}")
            print("---")
        await asyncio.sleep(1)  # Small delay between requests


if __name__ == "__main__":
    # Test single question
    print("=== Single Question Test ===")
    answer = asyncio.run(get_direct_answer("What is the capital of France?"))
    
    if answer:
        print(f"🎯 Final Answer: {answer}")
    
    # Test multiple questions
    print("\n=== Multiple Questions Test ===")
    asyncio.run(batch_questions())