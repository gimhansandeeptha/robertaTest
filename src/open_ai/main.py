## The logic to fetch the data from GPT and store them to the database/delete data ans all that(gpt table)
## also delete data if want 
from src.utils.data_model import ServicenowData
from src.open_ai.gpt import GPT
class APICall:
    def __init__(self) -> None:
        self.gpt = GPT()

    def _get_one_sentiment(self,comment):
        return self.gpt.get_response(comment)

    def set_gpt_sentiments(self, sn_data: ServicenowData):
        sn_data.reset_params()
        while sn_data.next_case():
            while sn_data.next_comment():
                comment = sn_data.get_comment()
                sentiment = self._get_one_sentiment(comment)
                sn_data.set_gpt_sentiment(sentiment)

