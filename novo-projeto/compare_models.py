#!/usr/bin/env python3
"""
Compare best models for backend analysis
"""

import os
import requests
import json

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    print("ERROR: Set OPENROUTER_API_KEY first")
    exit(1)

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit(1)

models = response.json()["data"]

# Filter: large context (100K+), not free tier
candidates = [
    m for m in models 
    if m.get("context_length", 0) >= 100000 
    and "free" not in m["id"].lower()
    and m.get("pricing", {}).get("prompt") is not None
]

# Sort by context size (desc), then price (asc)
candidates.sort(
    key=lambda x: (
        -x.get("context_length", 0),
        float(x["pricing"]["prompt"])
    )
)

print("=" * 80)
print("TOP 20 MODELS FOR BACKEND (Large Context + Good Pricing)")
print("=" * 80)
print()

for i, model in enumerate(candidates[:20], 1):
    ctx = model.get("context_length", 0)
    prompt_price = float(model["pricing"]["prompt"])
    completion_price = float(model["pricing"]["completion"])
    
    # Calculate cost per 1M tokens
    cost_1m_prompt = prompt_price * 1_000_000
    cost_1m_completion = completion_price * 1_000_000
    
    print(f"{i}. {model['id']}")
    print(f"   Context: {ctx:,} tokens")
    print(f"   Pricing: ${cost_1m_prompt:.2f} prompt / ${cost_1m_completion:.2f} completion per 1M tokens")
    print()

# Highlight recommendations
print("=" * 80)
print("RECOMMENDATIONS FOR ATIVO REAL BACKEND")
print("=" * 80)
print()

recommendations = {
    "ai21/jamba-large-1.7": "✅ CURRENT - Best cost/performance, 256K context, $9/1M tokens",
    "anthropic/claude-3.5-sonnet": "🎯 PREMIUM - Best reasoning for complex analysis, 200K context",
    "google/gemini-2.0-flash-exp": "⚡ FAST - Very fast, 1M context, experimental",
    "mistralai/mistral-large": "📊 TECHNICAL - Excellent for structured data, 128K context",
    "openai/gpt-4o": "💎 GOLD STANDARD - Highest quality, but expensive",
}

for model_id, desc in recommendations.items():
    match = next((m for m in models if m["id"] == model_id), None)
    if match:
        print(f"{model_id}")
        print(f"  {desc}")
        if match.get("context_length"):
            print(f"  Context: {match['context_length']:,} tokens")
        if match.get("pricing"):
            p = float(match["pricing"]["prompt"]) * 1_000_000
            c = float(match["pricing"]["completion"]) * 1_000_000
            print(f"  Cost: ${p:.2f} / ${c:.2f} per 1M tokens")
        print()
