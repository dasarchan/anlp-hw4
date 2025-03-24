import os
import time
import openai
from abc import ABC, abstractmethod


class Responser(ABC):

    @abstractmethod
    def respond(self, system_info: str, user_prompt: str) -> str:
        pass


class GPT4Responser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-4'):
        """ environment information """
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_base = os.environ.get("OPENAI_API_BASE")
        openai.api_type = 'azure'
        openai.api_version = '2023-07-01-preview'
        self.model = model

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        try:
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=2000,
                stop=None,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"{e}\nRate Limit Reached! Sleeping for 20 secs...")
            time.sleep(20)
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=2000,
                stop=None,
            )
            return response['choices'][0]['message']['content']


class TurboResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-3.5-turbo'):
        """ environment information """
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_base = os.environ.get("OPENAI_API_BASE")

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        messages = [
            {"role": "system", "content": system_info},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.ChatCompletion.create(
            # model='gpt-4',
            model='gpt-3.5-turbo',
            # model='gpt-4-32k',
            # model='gpt-3.5-turbo-16k',
            messages=messages
        )
        return response['choices'][0]['message']['content']


class LiteLLMResponser(Responser):
    """ LiteLLM responser for open-source models """

    def __init__(self, model_name="ollama/llama3", api_base=None):
        """
        Initialize with model name and optional API base URL
        :param model_name: Name of the model (e.g., 'ollama/llama3', 'huggingface/mistral-7b-instruct')
        :param api_base: Base URL for API calls (optional, depends on deployment)
        """
        import litellm
        self.litellm = litellm
        self.model_name = model_name
        
        # Set API base if provided
        if api_base:
            os.environ["OLLAMA_API_BASE"] = api_base
            # For other providers, you would set their specific environment variables

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        Generate a response using the specified open-source model
        :param system_info: System message/instructions
        :param user_prompt: User's input/query
        :return: Model's response as a string
        """
        try:
            messages = [
                {"role": "system", "content": system_info},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.litellm.completion(
                model=self.model_name,
                messages=messages,
                max_tokens=2000
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error with LiteLLM: {e}")
            time.sleep(1)  # Brief pause before retry
            try:
                response = self.litellm.completion(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_info},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=2000
                )
                return response['choices'][0]['message']['content']
            except Exception as e2:
                print(f"Second attempt failed: {e2}")
                return f"Error: Failed to generate response with {self.model_name}. Please check model availability and configuration."


if __name__ == '__main__':
    # gpt4_responser = GPT4Responser()
    # turbo_responser = TurboResponser()
    # print(turbo_responser.respond(system_info="Translate the text into English",
    #                               user_prompt=f"Elle a dit: \"Je suis une fille\""))
    
    litellm_responser = LiteLLMResponser(model_name="ollama/llama3:8b-instruct-fp16")
    print(litellm_responser.respond(system_info="Translate the text into English",
                                  user_prompt=f"Elle a dit: \"Je suis une fille\""))
