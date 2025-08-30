"""
Simple test script to verify XAgent integration
"""
import sys
import asyncio
import os
from pathlib import Path

# Add the integration directory to path
sys.path.append(str(Path(__file__).parent))

from xagent_integration import XAgentIntegration

async def test_xagent():
    """Test XAgent with a simple query"""
    print("Testing XAgent integration...")
    
    # Initialize XAgent integration
    xagent = XAgentIntegration()
    
    # Test with a simple query
    test_query = "What is the capital of France?"
    
    try:
        result = await xagent.run_xagent(test_query)
        print("✓ XAgent executed successfully!")
        print(f"Query: {test_query}")
        print(f"Answer: {result.get('answer', 'No answer found')}")
        print(f"Success: {result.get('success', False)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("Please check:")
        print("1. XAgent is properly cloned at ../XAgent/")
        print("2. You have required dependencies installed")
        print("3. XAgent's run.py is executable")

if __name__ == "__main__":
    asyncio.run(test_xagent())