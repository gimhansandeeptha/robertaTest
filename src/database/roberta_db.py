import pandas as pd
from src.database.main import Database
from src.utils.data_model import ServicenowData

class RobertaDB:
    def __init__(self) -> None:
        self.database = Database()
        self.entry_count_per_label = 10  # Set this value to actual value in the production
        self.max_entry_count_per_label = self.entry_count_per_label*7

    def insert_cases(self, sn_data:ServicenowData):
        # Insert the customer case comments to the database.
        sn_data.reset_params()
        while sn_data.next_case():
            case_id = sn_data.get_case_id()
            sys_created_on = sn_data.get_date()
            account_name = sn_data.get_account()
            self.database.insert_case(case_id, sys_created_on, account_name)
            while sn_data.next_comment():
                comment = sn_data.get_comment()
                sentiment = sn_data.get_sentiment()
                self.database.insert_case_comment(comment, sentiment, case_id)
                   
        # Delete excessive data in the database.

    def get_gpt_entries(self) -> pd.DataFrame:
        result = self.database.get_gpt_entries(self.entry_count_per_label)
        df = None
        if result is not None:
            df = pd.DataFrame(result, columns=['id','text', 'gpt_sentiment', 'datetime']) 
            df.dropna(inplace=True)
            # Ensure gpt_sentiment column has exactly three sentiment labels.
            valid_sentiments = ['Positive', 'Negative', 'Neutral']
            df = df[df['gpt_sentiment'].isin(valid_sentiments)]

            # Check the number of rows for each sentiment labels are equal to the "count"
            positive_count = (df['gpt_sentiment'] == valid_sentiments[0]).sum()
            negative_count = (df['gpt_sentiment'] == valid_sentiments[1]).sum()
            neutral_count = (df['gpt_sentiment'] == valid_sentiments[2]).sum()
            if positive_count == negative_count == neutral_count == self.entry_count_per_label:
                # Delete the data already fetched from the gpt table
                ids = df['id'].tolist()
                for id in ids:
                    self.database.delete_gpt_entry(id)
            else:
                df = None
        return df
    
    def insert_gpt_sentiment(self, sn_data:ServicenowData):
        # Inserting the new gpt sentiments to the database
        sn_data.reset_params()
        while sn_data.next_case():
            while sn_data.next_comment():
                text = sn_data.get_comment()
                gpt_sentiment = sn_data.get_gpt_sentiment()
                created_on = sn_data.get_date()
                self.database.insert_gpt_sentiment(text, gpt_sentiment, created_on)
        
        # After inserting delete the excessive data in the gpt table
        sentiment_count = self.database.get_sentiment_category_count()
        for sentiment, count in sentiment_count.items():
            count_to_delete = count - self.max_entry_count_per_label
            if count_to_delete > 0:
                self.database.delete_excessive_gpt_data(sentiment, count_to_delete)

    # The function to delete excessive case data(Probably for week ??) : To be implemented 
