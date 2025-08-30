"""
Mock XAgent integration for reliable testing
"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class MockXAgentIntegration:
    """Mock XAgent integration for testing"""
    
    async def run_xagent(self, task: str, **kwargs) -> Dict[str, Any]:
        """Mock XAgent execution"""
        # Simulate some processing time
        await asyncio.sleep(0.5)
        
        # Return mock responses based on the task
        if "capital" in task.lower() and "france" in task.lower():
            return {
                "answer": "The capital of France is Paris.",
                "steps": ["Query understanding", "Knowledge retrieval", "Response generation"],
                "success": True
            }
        elif "2+2" in task.lower() or "2 + 2" in task.lower():
            return {
                "answer": "2 + 2 = 4",
                "steps": ["Arithmetic calculation", "Result verification"],
                "success": True
            }
        else:
            return {
                "answer": f"I received your query: '{task}'. This is a mock response from the integrated XAgent system.",
                "steps": ["Query processing", "Mock response generation"],
                "success": True
            }
    
    def get_capabilities(self) -> List[str]:
        return ["mock_reasoning", "mock_tool_usage", "mock_web_search"]

# Singleton instance
xagent_integration = MockXAgentIntegration()