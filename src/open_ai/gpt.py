# API call implementation to the GPT
from openai import OpenAI
import asyncio

class GPT:
    def __init__(self) -> None:
        self.client = OpenAI(api_key="") 
        self.instruction = "You will be provided with a text, and your task is to classify its sentiment as positive, neutral, or negative."
        self.model = "gpt-3.5-turbo"
        self.instruction_role = "system"
        self.user_role = "user"
        self.temperature = 0.7
        self.max_tokens = 64
        self.top_p = 1

    def get_response(self, text:str):
        # response = self.client.chat.completions.create(
        #         model = self.model,
        #         messages = [
        #             {
        #                 "role" : self.instruction_role,
        #                 "content" : self.instruction
        #             },
        #             {
        #                 "role" : self.user_role,
        #                 "content" : text
        #             }
        #         ],
        #         temperature = self.temperature,
        #         max_tokens = self.max_tokens,
        #         top_p = self.top_p
        # )
        # return response.choices[0].message.content
        import random
        sentiments = ['Negative', 'Positive', 'Neutral']
        return random.choice(sentiments)


# Unit Testing
# text = "The case can be closed now. it is success and resolved. Thank you for your solution"
# gpt = GPT()
# sentiment = gpt.get_response(text)
# print(sentiment)
