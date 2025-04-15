import json
import os
import sys
import requests
from typing import Dict, List, Any, Optional, Callable, Union
from abc import ABC, abstractmethod
import openai

class LLMHandler(ABC):
    """
    Abstract base class for LLM handlers to use with the LLM Debug Agent.
    """
    
    @abstractmethod
    def __call__(
        self, 
        system_prompt: str, 
        conversation_history: List[Dict[str, Any]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Call the LLM model with the given prompt, conversation history, and tools.
        
        Args:
            system_prompt: The system prompt for the model
            conversation_history: The conversation history
            tools: The available tools
            
        Returns:
            Dict containing the model's response
        """
        pass

class Llama3Handler(LLMHandler):
    """
    A handler for the Llama3 model to use with the LLM Debug Agent.
    """
    
    def __init__(self, api_endpoint: str, api_key: Optional[str] = None):
        """
        Initialize the Llama3 handler.
        
        Args:
            api_endpoint: The endpoint for the Llama3 API
            api_key: Optional API key for authentication
        """
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        
    def __call__(
        self, 
        system_prompt: str, 
        conversation_history: List[Dict[str, Any]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Call the Llama3 model with the given prompt, conversation history, and tools.
        
        Args:
            system_prompt: The system prompt for the model
            conversation_history: The conversation history
            tools: The available tools
            
        Returns:
            Dict containing the model's response
        """
        # Prepare the request payload
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt}
            ] + conversation_history,
            "tools": tools
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Make the API request
        # NOTE: This is a placeholder - replace with your actual API call
        print(f"Would send request to {self.api_endpoint} with payload: {json.dumps(payload, indent=2)}")
        
        # Mock response - in real implementation, this would be:
        # response = requests.post(self.api_endpoint, json=payload, headers=headers)
        # return response.json()
        
        # For now, return a mock response that would execute the "start_debugging" tool
        return {
            "role": "assistant",
            "content": "I'll help you debug this code. Let me start the debugging session to examine the code.",
            "tool_calls": [
                {
                    "id": "call_abc123",
                    "type": "function",
                    "function": {
                        "name": "start_debugging",
                        "arguments": "{}"
                    }
                }
            ]
        }

class OpenAIHandler(LLMHandler):
    """
    A handler for OpenAI models to use with the LLM Debug Agent.
    """
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        """
        Initialize the OpenAI handler.
        
        Args:
            model: The OpenAI model to use (e.g., "gpt-4", "gpt-3.5-turbo")
            api_key: Optional API key for authentication
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided as an argument or as OPENAI_API_KEY environment variable")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
    def __call__(
        self, 
        system_prompt: str, 
        conversation_history: List[Dict[str, Any]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Call the OpenAI model with the given prompt, conversation history, and tools.
        
        Args:
            system_prompt: The system prompt for the model
            conversation_history: The conversation history
            tools: The available tools
            
        Returns:
            Dict containing the model's response
        """
        messages = [{"role": "system", "content": system_prompt}] + conversation_history
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            # Convert the OpenAI response to the expected format
            message = response.choices[0].message
            result = {
                "role": "assistant",
                "content": message.content or ""
            }
            
            # Include tool calls if present
            if message.tool_calls:
                result["tool_calls"] = []
                for tool_call in message.tool_calls:
                    result["tool_calls"].append({
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    })
            
            return result
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise