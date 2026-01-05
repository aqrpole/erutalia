# services/server/app/services/bedrock_client.py
import json
import re
import asyncio
import boto3
from typing                   import List
from app.core.config          import settings
from app.services.embed_local import generate_embeddings as local_generate_embeddings

# ---------- helpers ----------

def clean_response(text: str) -> str:
    if not text:
        return ""

    # Remove reasoning / thinking tags
    text = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL)
    text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def _get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=settings.BEDROCK_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

# ---------- LLM (chat) ----------

async def generate_response(prompt: str) -> str:
    """
    Generate a direct answer from Bedrock.
    No reasoning, no thinking, context-aware.
    """

    def _invoke():
        client = _get_bedrock_client()

        body = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. "
                        "Answer concisely and directly. "
                        "Do not include reasoning, thinking, or explanations."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_completion_tokens": 300,
            "temperature": 0.4,
            "top_p": 0.9,
        }

        response = client.invoke_model(
            modelId=settings.BEDROCK_MODEL_ID,
            body=json.dumps(body),
        )

        payload = json.loads(response["body"].read().decode("utf-8"))

        text = payload["choices"][0]["message"]["content"]
        return clean_response(text)

    # boto3 is blocking → run in thread
    return await asyncio.to_thread(_invoke)

# ---------- Embeddings ----------

async def generate_embeddings (text: str) -> List[float]:
    """
    Generate embeddings via Bedrock embedding model.
    """

    #def _invoke():
        #client = _get_bedrock_client()

        #body = {
        #    "inputText": text
        #}

        # future use when we have model generetor ID from aws bedrock (paid
        # thing)
        #response = client.invoke_model(
        #    modelId=settings.BEDROCK_EMBEDDING_MODEL_ID,
        #    body=json.dumps(body),
        #)
        #embeddings = await generate_embeddings (body)

        #payload = json.loads(response["body"].read().decode("utf-8"))
        #return payload["embedding"]

    #return await asyncio.to_thread(_invoke)
    if not text:
        return []

    # Local generator expects a list of strings
    embeddings = await local_generate_embeddings ([text])

    return embeddings[0]

async def health_check() -> bool:
    """
    Check if Bedrock Runtime is reachable.
    Uses a minimal invoke_model call.
    """

    def _check():
        try:
            client = boto3.client(
                service_name="bedrock-runtime",
                region_name=settings.BEDROCK_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

            # Minimal, low-cost request
            body = {
                "messages": [
                    {"role": "user", "content": "ping"}
                ],
                "max_completion_tokens": 1,
                "temperature": 0.0,
            }

            client.invoke_model(
                modelId=settings.BEDROCK_MODEL_ID,
                body=json.dumps(body),
            )

            return True

        except Exception as e:
            logger.error(f"❌ Bedrock health check failed: {e}")
            return False

    return await asyncio.to_thread(_check)
