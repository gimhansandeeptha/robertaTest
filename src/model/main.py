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
        self.model_creator: Model = None
        self.finetune_metadata_filepath = "models/finetune_checkpoint/metadata/roberta_metadata.json"
        self.stable_metadata_filepath = "models/stable_checkpoint/metadata/initial_metadata.json"
        self.max_finetuned_count = 5

    def train(self):
        pass

    def inference_process(self, sn_data: ServicenowData):
        metadata = Metadata(self.stable_metadata_filepath)
        model_path = metadata.get_value(["path"])
        model_creator = RobertaModel()
        model_creator.create()
        model_creator.load(model_path)

        sn_data.reset_params()
        while sn_data.next_case():
            while sn_data.next_comment():
                text = sn_data.get_comment()
                sentiment = model_creator.infer(text)
                sn_data.set_sentiment(sentiment)

    def finetune_process(self, df:pd.DataFrame):
        if df is not None:
            # print("Finetuning conditions are satisfied:", df.head())
            texts = df['text'].values
            sentiment = df["gpt_sentiment"].values

            sentiment_converter = RobertaSentimentConverter()
            sentiment_number = sentiment_converter.sentiment_to_num(sentiment)

            metadata = Metadata(self.finetune_metadata_filepath)
            checkpoint_path = metadata.get_value(['latest','path'])
            finetuned_count = metadata.get_value(['latest','finetune_count'])
            chekpoint_save_folder = metadata.get_value(['latest', 'checkpoint_save_folder'])

            model_creator = RobertaModel()
            model_creator.create()
            model_creator.load(checkpoint_path)

            # Finetuning 
            if finetuned_count < self.max_finetuned_count:
                model_creator.finetune(texts, sentiment_number)
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                new_checkpoint_path = os.path.join(chekpoint_save_folder, f"{current_datetime}.pth")
                model_creator.save(new_checkpoint_path)
                metadata.set_value(['latest','finetune_count'], finetuned_count+1)
                metadata.set_value(['latest','path'],new_checkpoint_path)
                os.remove(checkpoint_path)  

            # Validating                 
            else:
                checkpoint_validation_loss = model_creator.validate(texts, sentiment_number)
                stable_metadata = Metadata(self.stable_metadata_filepath)
                stable_model_path = stable_metadata.get_value(['path'])
                stable_save_folder = stable_metadata.get_value(['stable_save_folder'])
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                new_model_path = os.path.join(stable_save_folder, f"{current_datetime}.pth")
                stable_validation_loss = float(stable_metadata.get_value(['validation_loss']))

                # if new models loss is low it will be saved as the new stable model
                if checkpoint_validation_loss < stable_validation_loss:
                    model_creator.save(new_model_path)
                    os.remove(stable_model_path)
                    stable_metadata.set_value(['validation_loss'], checkpoint_validation_loss)
                    stable_metadata.set_value(['path'],new_model_path)
                else:
                    os.remove(checkpoint_path)  # Remove the finetuned model from the checkpoint folder if it is not improved 
                    metadata.set_value(['latest','path'], stable_model_path)# set the finetuned model path to the stable model 

                metadata.set_value(['latest','finetune_count'], 0)
        else:
            print("Finetuning conditions are not satisfied.")

# data = [
#             {
#                 "display_value": "CS0432475",
#                 "sys_id": "12307c011b050610d64e64a2604bcb23",
#                 "short_description": "State Flow Testing 2024/03/18 (09:05:01)",
#                 "number": "CS0432475",
#                 "entries": [
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:38:09",
#                         "sys_id": "2ad1925a1b654a90d64e64a2604bcbea",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:38:09",
#                         "contains_code": "false",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "Solution Accepted \n",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:37:10",
#                         "sys_id": "62d1925a1b654a90d64e64a2604bcbe9",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:37:10",
#                         "contains_code": "false",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "Proposed Solution Rejected \nI prefer different solution...",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:36:46",
#                         "sys_id": "fa90744d1b050610264c997a234bcb9c",
#                         "login_name": "Crypress User",
#                         "user_sys_id": "10377acb1bbcc250d64e64a2604bcbd3",
#                         "attachment": {
#                             "path": "fa90744d1b050610264c997a234bcb9c.iix",
#                             "sys_id": "fa90744d1b050610264c997a234bcb9c",
#                             "size_bytes": 172260,
#                             "content_type": "application/octet-stream",
#                             "size": "168 KB",
#                             "file_name": "AgentAttach_01.PNG",
#                             "state": "available"
#                         },
#                         "initials": "CU",
#                         "sys_created_on": "2024-03-18 03:36:46",
#                         "name": "Crypress User",
#                         "element": "attachment"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:36:11",
#                         "sys_id": "e67038c547410610a0a29cd3846d4319",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "attachment": {
#                             "path": "e67038c547410610a0a29cd3846d4319.iix",
#                             "sys_id": "e67038c547410610a0a29cd3846d4319",
#                             "size_bytes": 74348,
#                             "content_type": "application/octet-stream",
#                             "size": "72.6 KB",
#                             "file_name": "CustomerAttach_02.jpg",
#                             "state": "available"
#                         },
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:36:11",
#                         "name": "test new user",
#                         "element": "attachment"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:36:00",
#                         "sys_id": "e6d1925a1b654a90d64e64a2604bcbe7",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:36:00",
#                         "contains_code": "true",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "<p>Customer commented here..</p>",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:35:16",
#                         "sys_id": "62d1d25a1b654a90d64e64a2604bcb0b",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:35:16",
#                         "contains_code": "true",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "<br><b> <u>Description</u> </b><br><p></p><p>Test Description goes here</p><p></p>",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:35:15",
#                         "sys_id": "e040f8411b050610d64e64a2604bcbcb",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "attachment": {
#                             "path": "e040f8411b050610d64e64a2604bcbcb.iix",
#                             "sys_id": "e040f8411b050610d64e64a2604bcbcb",
#                             "size_bytes": 50389,
#                             "content_type": "application/octet-stream",
#                             "size": "49.2 KB",
#                             "file_name": "CustomerAttach_01.webp",
#                             "state": "available"
#                         },
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:35:15",
#                         "name": "test new user",
#                         "element": "attachment"
#                     }
#                 ],
#                 "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                 "user_full_name": "test new user",
#                 "user_login": "gimhans@wso2.com",
#                 "label": "Case",
#                 "table": "sn_customerservice_case",
#                 "journal_fields": [
#                     {
#                         "can_read": "true",
#                         "color": "transparent",
#                         "can_write": "true",
#                         "name": "comments",
#                         "label": "Additional comments"
#                     },
#                     {
#                         "can_read": "true",
#                         "color": "gold",
#                         "can_write": "true",
#                         "name": "work_notes",
#                         "label": "Work notes"
#                     }
#                 ],
#                 "sys_created_on": "2024-03-18 03:35:16",
#                 "sys_created_on_adjusted": "2024-03-18 03:35:16",
#                 "account": "ParaTestAccount1"
#             },
#             {
#                 "display_value": "CS0432476",
#                 "sys_id": "95f0740947410610a0a29cd3846d4362",
#                 "short_description": "Related Case : State Flow Testing 2024/03/18 (09:05:01)",
#                 "number": "CS0432476",
#                 "entries": [
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:38:41",
#                         "sys_id": "6ed1d25a1b654a90d64e64a2604bcb0f",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:38:41",
#                         "contains_code": "false",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "Closed by customer.",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:38:24",
#                         "sys_id": "a6d1d25a1b654a90d64e64a2604bcb15",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:38:24",
#                         "contains_code": "true",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "<br><b> <u>Description</u> </b><br><p>-- This is the previous description (Edit or Delete if you want to alter) --</p><p>Test Description goes here</p><p></p>",
#                         "element": "comments"
#                     }
#                 ],
#                 "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                 "user_full_name": "test new user",
#                 "user_login": "gimhans@wso2.com",
#                 "label": "Case",
#                 "table": "sn_customerservice_case",
#                 "journal_fields": [
#                     {
#                         "can_read": "true",
#                         "color": "transparent",
#                         "can_write": "true",
#                         "name": "comments",
#                         "label": "Additional comments"
#                     },
#                     {
#                         "can_read": "true",
#                         "color": "gold",
#                         "can_write": "true",
#                         "name": "work_notes",
#                         "label": "Work notes"
#                     }
#                 ],
#                 "sys_created_on": "2024-03-18 03:38:24",
#                 "sys_created_on_adjusted": "2024-03-18 03:38:24",
#                 "account": "ParaTestAccount2"
#             },
#             {
#                 "display_value": "CS0432478",
#                 "sys_id": "52a3f4091b050610d64e64a2604bcb33",
#                 "short_description": "State Flow Testing 2024/03/18 (09:20:03)",
#                 "number": "CS0432478",
#                 "entries": [
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:52:55",
#                         "sys_id": "26d1d25a1b654a90d64e64a2604bcb1c",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:52:55",
#                         "contains_code": "false",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "Solution Accepted \n",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:52:04",
#                         "sys_id": "22d1d25a1b654a90d64e64a2604bcb1b",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:52:04",
#                         "contains_code": "false",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "Proposed Solution Rejected \nI prefer different solution...",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:51:39",
#                         "sys_id": "c904f08d47410610a0a29cd3846d43f1",
#                         "login_name": "Crypress User",
#                         "user_sys_id": "10377acb1bbcc250d64e64a2604bcbd3",
#                         "attachment": {
#                             "path": "c904f08d47410610a0a29cd3846d43f1.iix",
#                             "sys_id": "c904f08d47410610a0a29cd3846d43f1",
#                             "size_bytes": 172260,
#                             "content_type": "application/octet-stream",
#                             "size": "168 KB",
#                             "file_name": "AgentAttach_01.PNG",
#                             "state": "available"
#                         },
#                         "initials": "CU",
#                         "sys_created_on": "2024-03-18 03:51:39",
#                         "name": "Crypress User",
#                         "element": "attachment"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:51:12",
#                         "sys_id": "9ee33c4d47410610a0a29cd3846d43b3",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "attachment": {
#                             "path": "9ee33c4d47410610a0a29cd3846d43b3.iix",
#                             "sys_id": "9ee33c4d47410610a0a29cd3846d43b3",
#                             "size_bytes": 74348,
#                             "content_type": "application/octet-stream",
#                             "size": "72.6 KB",
#                             "file_name": "CustomerAttach_02.jpg",
#                             "state": "available"
#                         },
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:51:12",
#                         "name": "test new user",
#                         "element": "attachment"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:51:01",
#                         "sys_id": "aad1d25a1b654a90d64e64a2604bcb19",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:51:01",
#                         "contains_code": "true",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "<p>Customer commented here..</p>",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:50:18",
#                         "sys_id": "26d1d25a1b654a90d64e64a2604bcb21",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:50:18",
#                         "contains_code": "true",
#                         "field_label": "Additional comments",
#                         "name": "test new user",
#                         "value": "<br><b> <u>Description</u> </b><br><p></p><p>Test Description goes here</p><p></p>",
#                         "element": "comments"
#                     },
#                     {
#                         "sys_created_on_adjusted": "2024-03-18 03:50:16",
#                         "sys_id": "acb338091b050610d64e64a2604bcb07",
#                         "login_name": "test new user",
#                         "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                         "attachment": {
#                             "path": "acb338091b050610d64e64a2604bcb07.iix",
#                             "sys_id": "acb338091b050610d64e64a2604bcb07",
#                             "size_bytes": 50389,
#                             "content_type": "application/octet-stream",
#                             "size": "49.2 KB",
#                             "file_name": "CustomerAttach_01.webp",
#                             "state": "available"
#                         },
#                         "initials": "TU",
#                         "sys_created_on": "2024-03-18 03:50:16",
#                         "name": "test new user",
#                         "element": "attachment"
#                     }
#                 ],
#                 "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
#                 "user_full_name": "test new user",
#                 "user_login": "gimhans@wso2.com",
#                 "label": "Case",
#                 "table": "sn_customerservice_case",
#                 "journal_fields": [
#                     {
#                         "can_read": True,
#                         "color": "transparent",
#                         "can_write": True,
#                         "name": "comments",
#                         "label": "Additional comments"
#                     },
#                     {
#                         "can_read": True,
#                         "color": "gold",
#                         "can_write": True,
#                         "name": "work_notes",
#                         "label": "Work notes"
#                     }
#                 ],
#                 "sys_created_on": "2024-03-18 03:50:18",
#                 "sys_created_on_adjusted": "2024-03-18 03:50:18",
#                 "account": "ParaTestAccount3"
#             }
#         ]

# sn_data = ServicenowData(data)
# sn_data.reset_params()
# model_process = ModelProcess()
# model_process.inference_process(sn_data)

# sn_data.reset_params()
# while sn_data.next_case():
#     while sn_data.next_comment():
#         print(sn_data.get_account(), sn_data.get_comment(), sn_data.get_sentiment())