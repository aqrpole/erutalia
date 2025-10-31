import boto3
import json
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env one folder up
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

async def test_bedrock_direct():
    """Test Bedrock with OpenAI GPT model"""
    try:
        print("🧪 Testing Bedrock OpenAI GPT model...")

        # Load configuration from environment
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("BEDROCK_REGION", "us-east-1")
        model_id = os.getenv("BEDROCK_MODEL_ID", "openai.gpt-oss-20b-1:0")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("Missing AWS credentials in .env file")

        print(f"Using model: {model_id}")
        print(f"Using region: {region}")

        # Create Bedrock client
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        # Create the request body for OpenAI GPT model
        native_request = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant for a university chatbot."
                },
                {
                    "role": "user", 
                    "content": "What is the capital of France?"
                }
            ],
            "max_completion_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.9
        }

        print(f"Request body: {json.dumps(native_request, indent=2)}")

        # Make the InvokeModel request
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(native_request)
        )

        # Parse and print the response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        print(f"✅ Raw Response: {json.dumps(response_body, indent=2)}")

        # Extract the assistant's message
        for choice in response_body['choices']:
            print(f"✅ Assistant: {choice['message']['content']}")
        
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


async def chat_with_assistant():
    """Chat with the assistant using proper message history"""
    try:
        print("🧪 Testing conversation with assistant role...")

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

        # Conversation with assistant role in history
        conversation = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful university assistant. Answer questions about courses, admissions, and campus life."
                },
                {
                    "role": "user",
                    "content": "Hello, I need help with course registration."
                },
                {
                    "role": "assistant",
                    "content": "Hello! I'd be happy to help you with course registration. What specific questions do you have?"
                },
                {
                    "role": "user", 
                    "content": "What are the computer science courses available this semester?"
                }
            ],
            "max_completion_tokens": 200,
            "temperature": 0.7
        }

        print("Sending conversation with assistant role...")
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(conversation)
        )

        response_body = json.loads(response['body'].read().decode('utf-8'))
        
        # Print the conversation
        print("\n📝 Conversation History:")
        for msg in conversation['messages']:
            print(f"{msg['role'].upper()}: {msg['content']}")
        
        print("\n🤖 Current Response:")
        for choice in response_body['choices']:
            print(f"ASSISTANT: {choice['message']['content']}")
        
        return True

    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False


if __name__ == "__main__":
    print("=== Test 1: Basic Question ===")
    success1 = asyncio.run(test_bedrock_direct())
    
    print("\n=== Test 2: Conversation with Assistant Role ===")
    success2 = asyncio.run(chat_with_assistant())
    
    if success1 and success2:
        print("🎯 All tests completed successfully!")
    else:
        print("💥 Some tests failed!")