#!/usr/bin/env python3
"""
Quick test de deployment do backend
"""

import requests
import json

# URL do SWA (onde o backend vai responder)
BASE_URL = "https://green-mud-007f89403.1.azurestaticapps.net"

print("=" * 60)
print("🚀 Testing ATIVO REAL Backend")
print("=" * 60)

tests = [
    {
        "name": "Health Check",
        "method": "GET",
        "endpoint": "/api/health",
        "data": None
    },
    {
        "name": "Database Connection",
        "method": "GET",
        "endpoint": "/api/projects",
        "data": None,
        "headers": {"Authorization": "Bearer test"}
    },
    {
        "name": "Login Test",
        "method": "POST",
        "endpoint": "/api/auth/login",
        "data": {
            "email": "topografo@bemreal.com",
            "password": "password"
        }
    }
]

for test in tests:
    try:
        url = f"{BASE_URL}{test['endpoint']}"
        headers = test.get("headers", {"Content-Type": "application/json"})
        
        if test["method"] == "GET":
            resp = requests.get(url, headers=headers, timeout=5)
        else:
            resp = requests.post(url, json=test["data"], headers=headers, timeout=5)
        
        status = "✅" if resp.status_code < 400 else "⚠️"
        print(f"\n{status} {test['name']}")
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.text[:100]}")
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ {test['name']}")
        print(f"   Connection failed - backend not yet deployed")
    except Exception as e:
        print(f"\n❌ {test['name']}")
        print(f"   Error: {str(e)[:100]}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
