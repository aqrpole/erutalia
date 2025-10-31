# services/server/scripts/test_bedrock_simple.py
import boto3
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

async def test_bedrock_direct():
    """Test Bedrock directly without app dependencies"""
    try:
        print("🧪 Testing Bedrock API directly...")
        api_key = os.getenv("BEDROCK_API_KEY")

        # Your configuration
        model_id = "openai.gpt-oss-20b-1:0"
        region = "us-east-2"

        # Create Bedrock client
        client = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=api_key,
            region_name=region,
        )

        # Test prompt
        prompt = "Hello! What is the capital of France?"

        # Try different request formats
        print("Testing with completion format...")
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 100,
            "temperature": 0.5,
        })

        response = client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response['body'].read())
        print(f"✅ Response: {response_body}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Trying alternative format...")

        # Try chat format
        try:
            body = json.dumps({
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100,
                "temperature": 0.5,
            })

            response = client.invoke_model(
                modelId=model_id,
                body=body,
                contentType="application/json", 
                accept="application/json"
            )

            response_body = json.loads(response['body'].read())
            print(f"✅ Chat format response: {response_body}")
            return True

        except Exception as e2:
            print(f"❌ Chat format also failed: {e2}")
            return False

if __name__ == "__main__":
    success = asyncio.run(test_bedrock_direct())
    print("🎯 Test completed successfully!" if success else "💥 All tests failed!")
