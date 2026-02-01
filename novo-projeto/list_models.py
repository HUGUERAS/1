#!/usr/bin/env python3
"""
List available models on OpenRouter
"""

import os
import json
import requests

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    print("ERROR: OPENROUTER_API_KEY not set")
    exit(1)

print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
print()

# List models
response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

if response.status_code == 200:
    models = response.json().get("data", [])
    
    print(f"Found {len(models)} models")
    print()
    
    # Filter for Jamba and Mistral models
    jamba_models = [m for m in models if "jamba" in m["id"].lower()]
    mistral_models = [m for m in models if "mistral" in m["id"].lower()]
    
    print("=== Jamba Models ===")
    for model in jamba_models:
        print(f"  - {model['id']}")
        if model.get("context_length"):
            print(f"    Context: {model['context_length']:,} tokens")
        if model.get("pricing"):
            print(f"    Pricing: ${model['pricing'].get('prompt', 0)} / ${model['pricing'].get('completion', 0)}")
    
    print()
    print("=== Mistral Models ===")
    for model in mistral_models[:5]:  # Top 5
        print(f"  - {model['id']}")
        if model.get("context_length"):
            print(f"    Context: {model['context_length']:,} tokens")
    
    print()
    print("=== All Models (first 20) ===")
    for model in models[:20]:
        print(f"  - {model['id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
