"""
Test different OpenAI models
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_model(model_name):
    """Test a specific OpenAI model."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ No API key found in .env file")
        return
    
    client = OpenAI(api_key=api_key)
    
    print(f"Testing model: {model_name}")
    print("-" * 40)
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "What are your capabilities?"}],
            max_tokens=100
        )
        
        print(f"✅ Success! Response:")
        print(f"Model: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Tokens: {response.usage.total_tokens}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("🤖 OpenAI Model Tester")
    print("=" * 40)
    
    # Models to test
    models = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4o"
    ]
    
    # Test each model
    results = {}
    for model in models:
        print(f"\nTesting {model}...")
        success = test_model(model)
        results[model] = "✅ Available" if success else "❌ Not available"
    
    # Summary
    print("\n" + "=" * 40)
    print("Model Availability Summary:")
    for model, status in results.items():
        print(f"{model}: {status}")
    
    # Update .env with working model
    working_models = [model for model, status in results.items() if "✅" in status]
    if working_models:
        print(f"\nTo use a specific model, update your .env file:")
        print(f"OPENAI_MODEL={working_models[0]}")

if __name__ == "__main__":
    main()