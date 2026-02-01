#!/usr/bin/env python3
"""
OpenRouter API Test - Detailed Error Reporting
"""

import os
import json
import sys
import requests

def test_openrouter():
    """Test OpenRouter API with detailed error information"""
    
    print("\n" + "="*70)
    print("OpenRouter API - Detailed Test")
    print("="*70 + "\n")
    
    # Get API key
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY not set")
        print("Set with: $env:OPENROUTER_API_KEY = 'key-here'")
        return False
    
    print(f"[OK] API Key found: {api_key[:20]}...{api_key[-10:]}")
    print(f"     Length: {len(api_key)} characters")
    print()
    
    # Test connectivity
    print("[TEST] Attempting to connect to OpenRouter API...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ativo-real.azure",
    }
    
    payload = {
        "model": "ai21/jamba-large-1.7",
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 50,
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"[HTTP] Status Code: {response.status_code}")
        print(f"[HTTP] Headers: {dict(response.headers)}")
        print()
        
        # Parse response
        try:
            response_json = response.json()
            print("[RESPONSE] Full JSON:")
            print(json.dumps(response_json, indent=2))
        except:
            print("[RESPONSE] Raw body:")
            print(response.text[:500])
        
        print()
        
        if response.status_code == 200:
            print("[SUCCESS] API is working!")
            return True
        elif response.status_code == 401:
            print("[ERROR] 401 Unauthorized - API key issue")
            print("  - Check if key is valid")
            print("  - Check if key has not expired")
            print("  - Check if OpenRouter account is active")
            return False
        elif response.status_code == 400:
            print("[ERROR] 400 Bad Request - Check payload")
            return False
        elif response.status_code == 429:
            print("[ERROR] 429 Rate Limited - Wait before retrying")
            return False
        else:
            print(f"[ERROR] Unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Connection failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_openrouter()
    sys.exit(0 if success else 1)
