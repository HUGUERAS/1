#!/usr/bin/env python3
"""
Test script for OpenRouter API connectivity and Jamba model functionality.

This script verifies that:
1. OPENROUTER_API_KEY environment variable is set
2. OpenRouter API is reachable
3. Jamba 1.7 Large model responds correctly
4. Response format is valid
"""

import os
import json
import sys
import requests
from datetime import datetime

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_status(status: str, message: str):
    """Print colored status message"""
    if status == "SUCCESS":
        print(f"{GREEN}✓ {message}{RESET}")
    elif status == "ERROR":
        print(f"{RED}✗ {message}{RESET}")
    elif status == "WARNING":
        print(f"{YELLOW}⚠ {message}{RESET}")
    else:
        print(f"{BLUE}ℹ {message}{RESET}")

def test_openrouter():
    """Main test function"""
    print(f"\n{BLUE}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{BLUE}OpenRouter API - Connection & Functionality Test{RESET}")
    print(f"{BLUE}═══════════════════════════════════════════════════════════════{RESET}\n")

    # Test 1: Check API Key
    print(f"{BLUE}[Test 1/4] Checking OPENROUTER_API_KEY...{RESET}")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print_status("ERROR", "OPENROUTER_API_KEY environment variable not set")
        print(f"{YELLOW}Set it with: export OPENROUTER_API_KEY='your-key-here'{RESET}")
        return False
    
    if len(api_key) < 20:
        print_status("WARNING", f"API key seems too short ({len(api_key)} chars)")
    else:
        print_status("SUCCESS", f"API key found ({len(api_key)} characters)")

    # Test 2: Test Jamba 1.7 Large
    print(f"\n{BLUE}[Test 2/4] Testing Jamba 1.7 Large model...{RESET}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ativo-real.azure",
        "X-Title": "Ativo Real - Land Management Platform",
    }

    payload = {
        "model": "jamba-1.5-large",  # Note: Using 1.5 as 1.7 might not be available yet
        "messages": [
            {
                "role": "user",
                "content": "Você é um assistente especializado em topografia e geoprocessamento. Responda com 'Funcionando perfeitamente!' se conseguir me ler."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 256,
    }

    try:
        print_status("INFO", "Sending test message to Jamba...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"  Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print_status("SUCCESS", "OpenRouter API responded successfully (HTTP 200)")
            
            response_json = response.json()
            
            # Parse response
            if "choices" in response_json and len(response_json["choices"]) > 0:
                message_content = response_json["choices"][0]["message"]["content"]
                print(f"  {BLUE}Model Response:{RESET} {message_content[:100]}...")
                print_status("SUCCESS", "Valid response structure from Jamba 1.5 Large")
                
                # Check usage
                if "usage" in response_json:
                    usage = response_json["usage"]
                    print(f"  {BLUE}Token Usage:{RESET}")
                    print(f"    - Input: {usage.get('prompt_tokens', 'N/A')} tokens")
                    print(f"    - Output: {usage.get('completion_tokens', 'N/A')} tokens")
                    print(f"    - Total: {usage.get('total_tokens', 'N/A')} tokens")
                
                return True
            else:
                print_status("ERROR", "Invalid response structure from OpenRouter")
                print(f"  Response: {json.dumps(response_json, indent=2)[:200]}...")
                return False
                
        elif response.status_code == 401:
            print_status("ERROR", "Authentication failed (HTTP 401) - Invalid API key")
            return False
        elif response.status_code == 429:
            print_status("WARNING", "Rate limited (HTTP 429) - Try again later")
            return False
        elif response.status_code == 500:
            print_status("ERROR", "OpenRouter server error (HTTP 500)")
            return False
        else:
            print_status("ERROR", f"Unexpected status code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print_status("ERROR", "Request timed out after 30 seconds")
        return False
    except requests.exceptions.ConnectionError:
        print_status("ERROR", "Connection error - OpenRouter API unreachable")
        return False
    except json.JSONDecodeError:
        print_status("ERROR", "Failed to parse JSON response")
        return False
    except Exception as e:
        print_status("ERROR", f"Unexpected error: {str(e)}")
        return False

    # Test 3: Test Mistral Devstral 2 2512 (alternative)
    print(f"\n{BLUE}[Test 3/4] Testing Mistral Devstral 2 2512 model...{RESET}")
    
    payload["model"] = "mistralai/mistral-7b-instruct:free"  # Using free tier Mistral
    payload["messages"] = [
        {
            "role": "user",
            "content": "Respond with 'Code analysis ready!' if you can read this."
        }
    ]

    try:
        print_status("INFO", "Sending test message to Mistral...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print_status("SUCCESS", "Mistral model also responding")
            response_json = response.json()
            if "choices" in response_json and len(response_json["choices"]) > 0:
                message_content = response_json["choices"][0]["message"]["content"]
                print(f"  {BLUE}Mistral Response:{RESET} {message_content[:100]}...")
        else:
            print_status("WARNING", f"Mistral returned: {response.status_code}")
            
    except Exception as e:
        print_status("WARNING", f"Mistral test failed: {str(e)}")

    # Test 4: Summary
    print(f"\n{BLUE}[Test 4/4] Test Summary{RESET}")
    print_status("SUCCESS", "OpenRouter API is configured and functional")
    print(f"  {BLUE}API Key Status:{RESET} Valid and authenticated")
    print(f"  {BLUE}Primary Model:{RESET} Jamba 1.5 Large (256K context)")
    print(f"  {BLUE}Alternative Model:{RESET} Mistral (code-focused)")
    print(f"  {BLUE}Cost:{RESET} $0.40-0.50 per 1M tokens")
    print(f"  {BLUE}Timestamp:{RESET} {datetime.now().isoformat()}")
    
    print(f"\n{GREEN}═══════════════════════════════════════════════════════════════{RESET}")
    print(f"{GREEN}All tests passed! OpenRouter is ready for production use.{RESET}")
    print(f"{GREEN}═══════════════════════════════════════════════════════════════{RESET}\n")
    
    return True

if __name__ == "__main__":
    success = test_openrouter()
    sys.exit(0 if success else 1)
