import os

import openai

from termgpt.models.base import ChatWithHistory


GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"  # if you have access...

class OpenAIChat(ChatWithHistory):
    """Class to handle chat with chatGPT, supports history and load from file"""

    def __init__(self, model_name=GPT3, file=None, resume=False, command=None, out_file=None, markdown=True):
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ImportError("[bold red]Please set `OPENAI_API_KEY` environment variable[/]")
        self.model_name=model_name
        # self.usage = OpenAIAPIStats(model_name=model_name)
        super().__init__(file=file, resume=resume, command=command, out_file=out_file, markdown=markdown)
    
    def call(self):
        r = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.history,
            stream=True
        )
        out = []

        for item in r:
            try:
                partial_result = item.choices[0].delta.content
                self.console.print(partial_result, end='')
                out.append(partial_result)
            except Exception as e:
                self.console.print()
            
        return ''.join(out)
    
    def save(self):
        super().save()
        # self.console.print(self.usage)