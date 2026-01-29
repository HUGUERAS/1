#!/usr/bin/env python3
"""
Dataset Validator for Fine-Tuning
Validates JSONL format, schema, and token limits
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Max tokens per sequence
MAX_TRAIN_TOKENS = 1024
MAX_TEST_TOKENS = 2048

def count_tokens(text: str) -> int:
    """Simple token estimation (actual tokenizer varies by model)"""
    return len(text.split())

def validate_message_format(message: Dict[str, Any]) -> tuple[bool, str]:
    """Validate individual message structure"""
    if not isinstance(message, dict):
        return False, "Message must be a dictionary"
    
    if 'role' not in message or 'content' not in message:
        return False, "Message must have 'role' and 'content' fields"
    
    if message['role'] not in ['user', 'assistant', 'system']:
        return False, f"Invalid role: {message['role']}"
    
    if not isinstance(message['content'], str):
        return False, "Content must be a string"
    
    return True, ""

def validate_jsonl_line(line: str, line_num: int, max_tokens: int) -> tuple[bool, str]:
    """Validate a single JSONL line"""
    try:
        data = json.loads(line)
    except json.JSONDecodeError as e:
        return False, f"Line {line_num}: Invalid JSON - {e}"
    
    # Check for 'messages' field
    if 'messages' not in data:
        return False, f"Line {line_num}: Missing 'messages' field"
    
    messages = data['messages']
    if not isinstance(messages, list) or len(messages) == 0:
        return False, f"Line {line_num}: 'messages' must be a non-empty list"
    
    # Validate each message
    total_tokens = 0
    for i, msg in enumerate(messages):
        valid, error = validate_message_format(msg)
        if not valid:
            return False, f"Line {line_num}, Message {i}: {error}"
        
        total_tokens += count_tokens(msg['content'])
    
    # Check token limit
    if total_tokens > max_tokens:
        return False, f"Line {line_num}: Too many tokens ({total_tokens} > {max_tokens})"
    
    return True, ""

def validate_dataset(file_path: str, dataset_type: str) -> bool:
    """Validate entire dataset file"""
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    if not path.suffix == '.json' and not path.suffix == '.jsonl':
        print(f"❌ File must have .json or .jsonl extension")
        return False
    
    max_tokens = MAX_TRAIN_TOKENS if dataset_type == 'train' else MAX_TEST_TOKENS
    
    print(f"🔍 Validating {dataset_type} dataset: {file_path}")
    print(f"   Max tokens per sample: {max_tokens}")
    
    errors = []
    valid_lines = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            
            valid, error = validate_jsonl_line(line, line_num, max_tokens)
            if valid:
                valid_lines += 1
            else:
                errors.append(error)
                if len(errors) >= 10:  # Stop after 10 errors
                    errors.append(f"... (stopping after 10 errors)")
                    break
    
    if errors:
        print(f"\n❌ Validation failed with {len(errors)} error(s):\n")
        for error in errors:
            print(f"   • {error}")
        return False
    
    print(f"\n✅ Validation successful!")
    print(f"   Valid samples: {valid_lines}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Validate fine-tuning datasets')
    parser.add_argument('--file', required=True, help='Path to dataset file')
    parser.add_argument('--type', required=True, choices=['train', 'test'], 
                       help='Dataset type (train or test)')
    
    args = parser.parse_args()
    
    success = validate_dataset(args.file, args.type)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
