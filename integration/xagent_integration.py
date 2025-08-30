import os
import sys
import subprocess
import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add XAgent to Python path
XAGENT_PATH = Path(__file__).parent.parent / "XAgent"
sys.path.append(str(XAGENT_PATH))

class XAgentIntegration:
    """Integration class to replace LangChain ReAct Agent with XAgent"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.xagent_home = XAGENT_PATH
        self.config_path = config_path or os.path.join(
            self.xagent_home, "config", "xagent_config.yaml"
        )
        
        # Verify XAgent installation
        self._verify_xagent_installation()
    
    def _verify_xagent_installation(self):
        """Verify that XAgent is properly installed and accessible"""
        required_files = [
            "run.py",
            "XAgent/__init__.py",
            "XAgent/core.py"
        ]
        
        for file in required_files:
            if not os.path.exists(os.path.join(self.xagent_home, file)):
                raise FileNotFoundError(
                    f"XAgent file not found: {file}. "
                    f"Please ensure XAgent is properly cloned at {self.xagent_home}"
                )
    
    async def run_xagent(self, task: str, **kwargs) -> Dict[str, Any]:
        """
        Run XAgent with a given task and return the result
        
        Args:
            task: The task description for XAgent
            **kwargs: Additional parameters for XAgent
            
        Returns:
            Dictionary containing XAgent's response
        """
        try:
            # Prepare command
            cmd = [
                sys.executable,
                str(self.xagent_home / "run.py"),
                "--task", task,
                "--config_file", self.config_path
            ]
            
            # Add additional parameters
            for key, value in kwargs.items():
                if value is not None:
                    cmd.extend([f"--{key}", str(value)])
            
            # Run XAgent
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=self.xagent_home,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip() or stdout.decode().strip()
                raise RuntimeError(f"XAgent execution failed: {error_msg}")
            
            # Parse XAgent output
            result = self._parse_xagent_output(stdout.decode())
            return result
            
        except Exception as e:
            raise RuntimeError(f"Error running XAgent: {str(e)}")
    
    def _parse_xagent_output(self, output: str) -> Dict[str, Any]:
        """
        Parse XAgent's output to extract the final answer
        
        Args:
            output: Raw output from XAgent
            
        Returns:
            Parsed result dictionary
        """
        # XAgent typically outputs JSON or structured text
        # This parsing might need adjustment based on XAgent's actual output format
        
        lines = output.strip().split('\n')
        result = {
            "raw_output": output,
            "answer": "",
            "steps": [],
            "success": True
        }
        
        # Try to find JSON output
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    json_data = json.loads(line)
                    if "answer" in json_data:
                        result["answer"] = json_data["answer"]
                    if "steps" in json_data:
                        result["steps"] = json_data["steps"]
                    break
                except json.JSONDecodeError:
                    continue
        
        # If no JSON found, use the last few lines as answer
        if not result["answer"]:
            result["answer"] = "\n".join(lines[-5:]) if len(lines) > 5 else output
        
        return result
    
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities that XAgent provides"""
        return [
            "reasoning",
            "tool_usage",
            "web_search",
            "code_execution",
            "problem_solving"
        ]

# Singleton instance for easy access
xagent_integration = XAgentIntegration()