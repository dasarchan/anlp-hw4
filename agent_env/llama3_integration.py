import json
import os
import sys
import requests
from typing import Dict, List, Any, Optional, Callable, Union
from abc import ABC, abstractmethod
import openai
import torch

# Import vLLM components for efficient inference
from vllm import LLM, SamplingParams
from vllm.utils import random_uuid

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
    A handler for the Llama 3.1 model using vLLM to use with the LLM Debug Agent.
    This implementation leverages vLLM for GPU-accelerated inference with tool calling.
    """
    
    def __init__(
        self,
        model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        gpu_memory_utilization: float = 0.9,
        max_model_len: int = 8192,
        tensor_parallel_size: int = 1,
        dtype: str = "bfloat16",
        # use_tool_calling: bool = True
    ):
        """
        Initialize the Llama 3.1 handler with vLLM.
        
        Args:
            model_name: HuggingFace model identifier
            gpu_memory_utilization: Fraction of GPU memory to use
            max_model_len: Maximum sequence length
            tensor_parallel_size: Number of GPUs to use
            dtype: Model precision (bfloat16, float16, or float32)
            use_tool_calling: Whether to enable tool calling functionality
        """
        # Convert string dtype to torch dtype
        if dtype == "bfloat16":
            torch_dtype = torch.bfloat16
        elif dtype == "float16":
            torch_dtype = torch.float16
        else:
            torch_dtype = torch.float32
            
        # Initialize vLLM model with GPU support
        self.model = LLM(
            model=model_name,
            tensor_parallel_size=tensor_parallel_size,
            gpu_memory_utilization=gpu_memory_utilization,
            max_model_len=max_model_len,
            dtype=torch_dtype,
            trust_remote_code=True,
            # enable_tool_calls=use_tool_calling,
            # tool_call_parser="llama3_json",
        )
        
        # self.use_tool_calling = use_tool_calling
        
    def __call__(
        self, 
        system_prompt: str, 
        conversation_history: List[Dict[str, Any]],
        tools: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Call the Llama 3.1 model with the given prompt, conversation history, and tools.
        Uses vLLM for efficient inference with GPU acceleration.
        
        Args:
            system_prompt: The system prompt for the model
            conversation_history: The conversation history
            tools: The available tools
            
        Returns:
            Dict containing the model's response
        """
        # Prepare the full message list with system prompt
        messages = [{"role": "system", "content": system_prompt}] + conversation_history
        
        # Format prompts for vLLM
        from transformers import AutoTokenizer
        
        # Load the tokenizer for the model to apply chat template
        tokenizer = AutoTokenizer.from_pretrained(self.model.llm_engine.model_config.hf_config.name_or_path)
        formatted_prompt = tokenizer.apply_chat_template(
            messages, 
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Set up sampling parameters for inference
        sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.95,
            max_tokens=1024,
            stop_token_ids=[tokenizer.eos_token_id],
        )
        
        # If using tool calling, add tool specification
        # if tools:
        #     # Configure sampling params with tool specification
        #     sampling_params = SamplingParams(
        #         temperature=0.7,
        #         top_p=0.95,
        #         max_tokens=1024,
        #         stop_token_ids=[tokenizer.eos_token_id],
        #         tool_choices=tools
        #     )
            
        # Generate completion using vLLM
        outputs = self.model.chat(
            messages,
            sampling_params=sampling_params,
            tools=tools
        )
        
        # Process the output
        raw_output = outputs[0].outputs[0].text
        
        # Parse the response to extract content and potential tool calls
        result = {
            "role": "assistant",
            "content": raw_output
        }
        
        # Extract tool calls if present
        # Note: vLLM's tool parser should handle most of this, but we need to 
        # extract the structured response format here
        if "Action:" in raw_output:
            # Simple parsing for tool calls in the format:
            # Action: tool_name
            # Action Input: {"param1": "value1"}
            lines = raw_output.split('\n')
            tool_name = None
            tool_args = None
            
            for line in lines:
                if line.startswith("Action:"):
                    tool_name = line.replace("Action:", "").strip()
                elif line.startswith("Action Input:"):
                    tool_args = line.replace("Action Input:", "").strip()
            
            if tool_name and tool_args:
                try:
                    # For JSON-formatted arguments
                    tool_args_dict = json.loads(tool_args)
                    
                    # Format the tool call in the expected structure
                    result["tool_calls"] = [{
                        "id": f"call_{random_uuid()}",
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(tool_args_dict)
                        }
                    }]
                    
                    # Remove the tool calling syntax from the content
                    clean_content = raw_output
                    for line in lines:
                        if line.startswith("Action:") or line.startswith("Action Input:"):
                            clean_content = clean_content.replace(line, "")
                    result["content"] = clean_content.strip()
                    
                except json.JSONDecodeError:
                    # If the arguments aren't valid JSON, keep the original output
                    pass
        
        return result

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