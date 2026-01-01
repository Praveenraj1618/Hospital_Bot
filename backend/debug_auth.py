"""
Debug script to check authentication configuration
Run this to verify SECRET_KEY is loaded correctly
"""
import os
from dotenv import load_dotenv

print("=" * 60)
print("AUTHENTICATION DEBUG")
print("=" * 60)

# Load .env
load_dotenv()

# Check .env file exists
env_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"\n1. .env file exists: {os.path.exists(env_path)}")
if os.path.exists(env_path):
    print(f"   Path: {env_path}")
    with open(env_path, 'r') as f:
        content = f.read()
        print(f"   Content preview: {content[:100]}...")

# Check SECRET_KEY
secret_key = os.getenv("SECRET_KEY")
print(f"\n2. SECRET_KEY from environment:")
print(f"   Set: {secret_key is not None}")
if secret_key:
    print(f"   Length: {len(secret_key)}")
    print(f"   First 20 chars: {secret_key[:20]}...")
else:
    print("   ⚠️  SECRET_KEY is NOT SET in environment!")

# Check DATABASE_URL
db_url = os.getenv("DATABASE_URL")
print(f"\n3. DATABASE_URL from environment:")
print(f"   Set: {db_url is not None}")
if db_url:
    # Hide password in output
    safe_url = db_url.split("@")[-1] if "@" in db_url else db_url
    print(f"   Database: {safe_url}")

# Check ACCESS_TOKEN_EXPIRE_MINUTES
expire_min = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
print(f"\n4. ACCESS_TOKEN_EXPIRE_MINUTES:")
print(f"   Value: {expire_min}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
if not secret_key or secret_key == "your-secret-key-change-this-in-production-use-environment-variable":
    print("WARNING: SECRET_KEY is using default value!")
    print("   Make sure your .env file has a proper SECRET_KEY")
else:
    print("OK: SECRET_KEY is loaded from .env")
    print("   If you're still getting 401 errors:")
    print("   1. Make sure backend was RESTARTED after creating .env")
    print("   2. Clear localStorage and log in again to get fresh token")
print("=" * 60)

