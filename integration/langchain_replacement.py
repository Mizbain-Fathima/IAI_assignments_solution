"""
Replacement module for LangChain ReAct Agent using XAgent
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Use absolute import instead of relative
import sys
from pathlib import Path

# Add the current directory to path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from xagent_integration import xagent_integration

@dataclass
class AgentResponse:
    """Standardized response format to match LangChain's output"""
    output: str
    intermediate_steps: List[Any] = None
    success: bool = True
    error_message: Optional[str] = None

class XAgentWrapper:
    """Wrapper class to replace LangChain's ReAct Agent"""
    
    def __init__(self, tools: Optional[List[Any]] = None, **kwargs):
        self.tools = tools or []
        self.config = kwargs
        self.capabilities = xagent_integration.get_capabilities()
    
    async def arun(self, input_text: str, **kwargs) -> AgentResponse:
        """Async run method to match LangChain interface"""
        return await self.run(input_text, **kwargs)
    
    async def run(self, input_text: str, **kwargs) -> AgentResponse:
        """Execute XAgent with the given input"""
        try:
            # Merge instance config with runtime kwargs
            execution_config = {**self.config, **kwargs}
            
            # Run XAgent
            result = await xagent_integration.run_xagent(input_text, **execution_config)
            
            return AgentResponse(
                output=result.get("answer", ""),
                intermediate_steps=result.get("steps", []),
                success=result.get("success", True)
            )
            
        except Exception as e:
            return AgentResponse(
                output=f"Error: {str(e)}",
                success=False,
                error_message=str(e)
            )
    
    def __call__(self, input_text: str, **kwargs) -> AgentResponse:
        """Sync call method for compatibility"""
        try:
            # Create a new event loop if none exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            return loop.run_until_complete(self.run(input_text, **kwargs))
        except Exception as e:
            return AgentResponse(
                output=f"Error: {str(e)}",
                success=False,
                error_message=str(e)
            )

# Factory function to replace LangChain's agent initialization
def initialize_xagent(tools: List[Any] = None, **kwargs) -> XAgentWrapper:
    """
    Factory function to create XAgent instances
    Replaces LangChain's initialize_agent function
    """
    return XAgentWrapper(tools=tools, **kwargs)