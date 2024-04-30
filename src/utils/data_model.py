import pandas as pd 
import numpy as np
from datetime import datetime

class DatabaseData:
    def __init__(self) -> None:
        self.data: pd.DataFrame = None
        self.iter_index = 0

    def load_data(self, data): 
        pass

    def load_test_data(self, df):
        self.data = df

    def insert_field(self, column_name:str):
        if column_name not in self.data.columns:
            self.data[column_name] = None
            return True
        else:
            return False
    
    def insert_data(self, index, column_name, value):
        if self.data.at[index, column_name] is None:
            self.data.at[index, column_name] = value
        else:
            raise UserWarning("Trying to modify exsisting value")
        
    def get_data(self, index:int):
        if self.data is not None and self.iter_index < len(self.data):
            row = self.data.iloc[index]
            return row
        else:
            return None
    
    def get_data(self, index:int, columns:list):
        if self.data is not None and index < len(self.data):
            return self.data.loc[index, columns]
        else:
            return None
        
    def get_data(self):
        return self.data
    
    def get_column(self, column_name:str) -> np.array:
        column_array = self.data[column_name].to_numpy()
        return column_array
    
    def filed_names(self)->list:
        if self.data is not None:
            return self.data.columns.tolist()
        else:
            return None

class ServicenowData:
    def load_data(self, data:list[dict]) -> None:
        self.data = data
        self.length = len(data)
        self.reset_params()

    def reset_params(self):
        "Call this function before iterating through the data"
        self.case_no=-1
        self.comment_no= -1
        self.current_case:dict = None
        self.entries:list[dict] = None
        self.comment:str = None

    def next_case(self) -> bool:
        if self.case_no < self.length-1:
            self.case_no +=1
            self.current_case = self.data[self.case_no]
            self.entries = self.current_case.get("entries")
            self.comment_no = -1
            return True
        else:
            return False
        
    def next_comment(self) -> bool:
        if self.comment_no < len(self.entries)-1:
            self.comment_no +=1
            self.comment = self.entries[self.comment_no].get("value", None)
            if self.comment is not None:
                return True
            else:
                return self.next_comment()
        else:
            return False
        
    def get_case_id(self):
        case_id = self.current_case.get("case_id")
        return case_id
    
    def get_account(self):
        account = self.current_case.get("account")
        return account
    
    def get_date(self):
        sys_created = self.current_case.get("sys_created_on", datetime.now())
        return sys_created
    
    def get_case(self):
        return self.current_case
    
    def get_comment(self):
        return self.comment
    
    def get_sentiment(self):
        sentiment = self.entries[self.comment_no].get("sentiment", "")
        return sentiment
    
    def get_gpt_sentiment(self):
        gpt_sentiment = self.entries[self.comment_no].get("gpt_sentiment","")
        return gpt_sentiment
    
    def set_comment(self, comment:str):
        self.comment = comment
        self.entries[self.comment_no]["value"] = self.comment

    def set_sentiment(self, sentiment:str):
        self.entries[self.comment_no]["sentiment"] = sentiment

    def set_gpt_sentiment(self, sentiment:str):
        self.entries[self.comment_no]["gpt_sentiment"] = sentiment
        
        
data = [
            {
                "display_value": "CS0432475",
                "sys_id": "12307c011b050610d64e64a2604bcb23",
                "short_description": "State Flow Testing 2024/03/18 (09:05:01)",
                "number": "CS0432475",
                "entries": [
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:38:09",
                        "sys_id": "2ad1925a1b654a90d64e64a2604bcbea",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:38:09",
                        "contains_code": "false",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "Solution Accepted \n",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:37:10",
                        "sys_id": "62d1925a1b654a90d64e64a2604bcbe9",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:37:10",
                        "contains_code": "false",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "Proposed Solution Rejected \nI prefer different solution...",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:36:46",
                        "sys_id": "fa90744d1b050610264c997a234bcb9c",
                        "login_name": "Crypress User",
                        "user_sys_id": "10377acb1bbcc250d64e64a2604bcbd3",
                        "attachment": {
                            "path": "fa90744d1b050610264c997a234bcb9c.iix",
                            "sys_id": "fa90744d1b050610264c997a234bcb9c",
                            "size_bytes": 172260,
                            "content_type": "application/octet-stream",
                            "size": "168 KB",
                            "file_name": "AgentAttach_01.PNG",
                            "state": "available"
                        },
                        "initials": "CU",
                        "sys_created_on": "2024-03-18 03:36:46",
                        "name": "Crypress User",
                        "element": "attachment"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:36:11",
                        "sys_id": "e67038c547410610a0a29cd3846d4319",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "attachment": {
                            "path": "e67038c547410610a0a29cd3846d4319.iix",
                            "sys_id": "e67038c547410610a0a29cd3846d4319",
                            "size_bytes": 74348,
                            "content_type": "application/octet-stream",
                            "size": "72.6 KB",
                            "file_name": "CustomerAttach_02.jpg",
                            "state": "available"
                        },
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:36:11",
                        "name": "test new user",
                        "element": "attachment"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:36:00",
                        "sys_id": "e6d1925a1b654a90d64e64a2604bcbe7",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:36:00",
                        "contains_code": "true",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "<p>Customer commented here..</p>",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:35:16",
                        "sys_id": "62d1d25a1b654a90d64e64a2604bcb0b",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:35:16",
                        "contains_code": "true",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "<br><b> <u>Description</u> </b><br><p></p><p>Test Description goes here</p><p></p>",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:35:15",
                        "sys_id": "e040f8411b050610d64e64a2604bcbcb",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "attachment": {
                            "path": "e040f8411b050610d64e64a2604bcbcb.iix",
                            "sys_id": "e040f8411b050610d64e64a2604bcbcb",
                            "size_bytes": 50389,
                            "content_type": "application/octet-stream",
                            "size": "49.2 KB",
                            "file_name": "CustomerAttach_01.webp",
                            "state": "available"
                        },
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:35:15",
                        "name": "test new user",
                        "element": "attachment"
                    }
                ],
                "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                "user_full_name": "test new user",
                "user_login": "gimhans@wso2.com",
                "label": "Case",
                "table": "sn_customerservice_case",
                "journal_fields": [
                    {
                        "can_read": "true",
                        "color": "transparent",
                        "can_write": "true",
                        "name": "comments",
                        "label": "Additional comments"
                    },
                    {
                        "can_read": "true",
                        "color": "gold",
                        "can_write": "true",
                        "name": "work_notes",
                        "label": "Work notes"
                    }
                ],
                "sys_created_on": "2024-03-18 03:35:16",
                "sys_created_on_adjusted": "2024-03-18 03:35:16",
                "account": "ParaTestAccount1"
            },
            {
                "display_value": "CS0432476",
                "sys_id": "95f0740947410610a0a29cd3846d4362",
                "short_description": "Related Case : State Flow Testing 2024/03/18 (09:05:01)",
                "number": "CS0432476",
                "entries": [
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:38:41",
                        "sys_id": "6ed1d25a1b654a90d64e64a2604bcb0f",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:38:41",
                        "contains_code": "false",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "Closed by customer.",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:38:24",
                        "sys_id": "a6d1d25a1b654a90d64e64a2604bcb15",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:38:24",
                        "contains_code": "true",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "<br><b> <u>Description</u> </b><br><p>-- This is the previous description (Edit or Delete if you want to alter) --</p><p>Test Description goes here</p><p></p>",
                        "element": "comments"
                    }
                ],
                "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                "user_full_name": "test new user",
                "user_login": "gimhans@wso2.com",
                "label": "Case",
                "table": "sn_customerservice_case",
                "journal_fields": [
                    {
                        "can_read": "true",
                        "color": "transparent",
                        "can_write": "true",
                        "name": "comments",
                        "label": "Additional comments"
                    },
                    {
                        "can_read": "true",
                        "color": "gold",
                        "can_write": "true",
                        "name": "work_notes",
                        "label": "Work notes"
                    }
                ],
                "sys_created_on": "2024-03-18 03:38:24",
                "sys_created_on_adjusted": "2024-03-18 03:38:24",
                "account": "ParaTestAccount2"
            },
            {
                "display_value": "CS0432478",
                "sys_id": "52a3f4091b050610d64e64a2604bcb33",
                "short_description": "State Flow Testing 2024/03/18 (09:20:03)",
                "number": "CS0432478",
                "entries": [
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:52:55",
                        "sys_id": "26d1d25a1b654a90d64e64a2604bcb1c",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:52:55",
                        "contains_code": "false",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "Solution Accepted \n",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:52:04",
                        "sys_id": "22d1d25a1b654a90d64e64a2604bcb1b",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:52:04",
                        "contains_code": "false",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "Proposed Solution Rejected \nI prefer different solution...",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:51:39",
                        "sys_id": "c904f08d47410610a0a29cd3846d43f1",
                        "login_name": "Crypress User",
                        "user_sys_id": "10377acb1bbcc250d64e64a2604bcbd3",
                        "attachment": {
                            "path": "c904f08d47410610a0a29cd3846d43f1.iix",
                            "sys_id": "c904f08d47410610a0a29cd3846d43f1",
                            "size_bytes": 172260,
                            "content_type": "application/octet-stream",
                            "size": "168 KB",
                            "file_name": "AgentAttach_01.PNG",
                            "state": "available"
                        },
                        "initials": "CU",
                        "sys_created_on": "2024-03-18 03:51:39",
                        "name": "Crypress User",
                        "element": "attachment"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:51:12",
                        "sys_id": "9ee33c4d47410610a0a29cd3846d43b3",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "attachment": {
                            "path": "9ee33c4d47410610a0a29cd3846d43b3.iix",
                            "sys_id": "9ee33c4d47410610a0a29cd3846d43b3",
                            "size_bytes": 74348,
                            "content_type": "application/octet-stream",
                            "size": "72.6 KB",
                            "file_name": "CustomerAttach_02.jpg",
                            "state": "available"
                        },
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:51:12",
                        "name": "test new user",
                        "element": "attachment"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:51:01",
                        "sys_id": "aad1d25a1b654a90d64e64a2604bcb19",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:51:01",
                        "contains_code": "true",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "<p>Customer commented here..</p>",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:50:18",
                        "sys_id": "26d1d25a1b654a90d64e64a2604bcb21",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:50:18",
                        "contains_code": "true",
                        "field_label": "Additional comments",
                        "name": "test new user",
                        "value": "<br><b> <u>Description</u> </b><br><p></p><p>Test Description goes here</p><p></p>",
                        "element": "comments"
                    },
                    {
                        "sys_created_on_adjusted": "2024-03-18 03:50:16",
                        "sys_id": "acb338091b050610d64e64a2604bcb07",
                        "login_name": "test new user",
                        "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                        "attachment": {
                            "path": "acb338091b050610d64e64a2604bcb07.iix",
                            "sys_id": "acb338091b050610d64e64a2604bcb07",
                            "size_bytes": 50389,
                            "content_type": "application/octet-stream",
                            "size": "49.2 KB",
                            "file_name": "CustomerAttach_01.webp",
                            "state": "available"
                        },
                        "initials": "TU",
                        "sys_created_on": "2024-03-18 03:50:16",
                        "name": "test new user",
                        "element": "attachment"
                    }
                ],
                "user_sys_id": "65965cec47e475d0a0a29cd3846d43d9",
                "user_full_name": "test new user",
                "user_login": "gimhans@wso2.com",
                "label": "Case",
                "table": "sn_customerservice_case",
                "journal_fields": [
                    {
                        "can_read": True,
                        "color": "transparent",
                        "can_write": True,
                        "name": "comments",
                        "label": "Additional comments"
                    },
                    {
                        "can_read": True,
                        "color": "gold",
                        "can_write": True,
                        "name": "work_notes",
                        "label": "Work notes"
                    }
                ],
                "sys_created_on": "2024-03-18 03:50:18",
                "sys_created_on_adjusted": "2024-03-18 03:50:18",
                "account": "ParaTestAccount3"
            }
        ]

# sn_data = ServicenowData(data)
# sn_data.reset_params()

# i=0
# while sn_data.next_case():
#     while sn_data.next_comment():
#         i+=1
#         print(sn_data.get_account(), sn_data.get_comment())
#         sn_data.set_comment(f"This comment is set to {i}")
#         sn_data.set_sentiment("Positive")

# print("------------------------------------------------------------")
# sn_data.reset_params()
# while sn_data.next_case():
#     while sn_data.next_comment():
#         print(sn_data.get_account(), sn_data.get_comment(), sn_data.get_sentiment(), sn_data.get_gpt_sentiment())

# print("------------------------------------------------------------")

# print(sn_data.data)

