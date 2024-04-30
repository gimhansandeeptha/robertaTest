import os
from datetime import datetime
import pandas as pd
from src.model.models.model import Model
from src.model.models.roberta_model import RobertaModel
from src.utils.metadata import Metadata
from src.utils.data_model import ServicenowData, DatabaseData
from src.model.preprocess.roberta_dataloader import RobertaTrainSentimentData
from src.model.preprocess.roberta_sentiment_converter import RobertaSentimentConverter

class ModelProcess:
    def __init__(self):
        """ max_finetuned_count: Number of finetuning iterations before the validation phase. 
                                Do not confuse this with the epochs for a perticular finetuninig.
            finetune_metadata_filepath: Metadata file path for partially finetuned models.
            stable_metadata_filepath: Metadata file for stable model(inferencing model)
        """
        self.model_creator: RobertaModel = None
        self.model_checkpoint_path = "./src/checkpoint/your_model.pth"
        self.max_finetuned_count = 5

    def train(self):
        pass

    def inference_process(self):
        self.model_creator = RobertaModel()
        self.model_creator.create()
        self.model_creator.load(self.model_checkpoint_path)
    
    def inference(self, text):
        sentiment = self.model_creator.infer(text)
        return sentiment
    
    def finetune_process(self, df:pd.DataFrame):
        pass
        # if df is not None:
        #     # print("Finetuning conditions are satisfied:", df.head())
        #     texts = df['text'].values
        #     sentiment = df["gpt_sentiment"].values

        #     sentiment_converter = RobertaSentimentConverter()
        #     sentiment_number = sentiment_converter.sentiment_to_num(sentiment)

        #     metadata = Metadata(self.finetune_metadata_filepath)
        #     checkpoint_path = metadata.get_value(['latest','path'])
        #     finetuned_count = metadata.get_value(['latest','finetune_count'])
        #     chekpoint_save_folder = metadata.get_value(['latest', 'checkpoint_save_folder'])

        #     model_creator = RobertaModel()
        #     model_creator.create()
        #     model_creator.load(checkpoint_path)

        #     # Finetuning 
        #     if finetuned_count < self.max_finetuned_count:
        #         model_creator.finetune(texts, sentiment_number)
        #         current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #         new_checkpoint_path = os.path.join(chekpoint_save_folder, f"{current_datetime}.pth")
        #         model_creator.save(new_checkpoint_path)
        #         metadata.set_value(['latest','finetune_count'], finetuned_count+1)
        #         metadata.set_value(['latest','path'],new_checkpoint_path)
        #         os.remove(checkpoint_path)  

        #     # Validating                 
        #     else:
        #         checkpoint_validation_loss = model_creator.validate(texts, sentiment_number)
        #         stable_metadata = Metadata(self.stable_metadata_filepath)
        #         stable_model_path = stable_metadata.get_value(['path'])
        #         stable_save_folder = stable_metadata.get_value(['stable_save_folder'])
        #         current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #         new_model_path = os.path.join(stable_save_folder, f"{current_datetime}.pth")
        #         stable_validation_loss = float(stable_metadata.get_value(['validation_loss']))

        #         # if new models loss is low it will be saved as the new stable model
        #         if checkpoint_validation_loss < stable_validation_loss:
        #             model_creator.save(new_model_path)
        #             os.remove(stable_model_path)
        #             stable_metadata.set_value(['validation_loss'], checkpoint_validation_loss)
        #             stable_metadata.set_value(['path'],new_model_path)
        #         else:
        #             os.remove(checkpoint_path)  # Remove the finetuned model from the checkpoint folder if it is not improved 
        #             metadata.set_value(['latest','path'], stable_model_path)# set the finetuned model path to the stable model 

        #         metadata.set_value(['latest','finetune_count'], 0)
        # else:
        #     print("Finetuning conditions are not satisfied.")
