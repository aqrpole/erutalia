import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env one folder up
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

def verify_aws_credentials():
    """Test if AWS credentials are valid"""

    # Load configuration from environment
    api_key = os.getenv("BEDROCK_API_KEY")
    region = os.getenv("BEDROCK_REGION", "us-east-2")
    model_id = os.getenv("BEDROCK_MODEL_ID", "openai.gpt-oss-20b-1:0")
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")       
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")    
    
    try:
        # Test with a simple service
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✅ AWS Credentials Valid")
        print(f"   Account: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        return True
    except Exception as e:
        print(f"❌ AWS Credentials Invalid: {e}")
        return False

# Set your credentials (choose one method)
# Method 1: Environment variables
os.environ['AWS_ACCESS_KEY_ID'] =os.getenv("AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY'] =os.getenv("AWS_SECRET_ACCESS_KEY") 
os.environ['AWS_REGION'] = 'us-east-2'

# Method 2: AWS credentials file (~/.aws/credentials)
# Method 3: IAM role (if running on EC2)

verify_aws_credentials()