import torch
import numpy as np
from tqdm import tqdm
from transformers import RobertaTokenizer
from torch.utils.data import DataLoader
from model.models.model import Model
from model.models.finetune.roberta_finetune import RobertaFinetune
from model.models.validate.roberta_validate import RobertaValidate
from model.models.roberta import RobertaClass
from model.models.inference.roberta_inference import RobertaInference
from model.preprocess.roberta_dataloader import RobertaInferenceSentimentData, RobertaTrainSentimentData
from utils.data_model import ServicenowData

"""Concreate factory for Roberta models"""
class RobertaModel(Model):
    def __init__(self) -> None:
        self.model: torch.nn.Module = None
        self.tokenizer = None
        self.loss_function = None
        self.optimizer = None
        self.max_len = 256
        self.device = "cpu"
        self.finetune_batch_size = 32
    
    def create(self):
        model = RobertaClass()
        self.model = model

        tokenizer = RobertaTokenizer.from_pretrained('roberta-base', truncation=True, do_lower_case=True)
        self.tokenizer = tokenizer

        loss_function = torch.nn.CrossEntropyLoss()
        self.loss_function = loss_function

        LEARNING_RATE = 1e-05
        optimizer = torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)
        self.optimizer = optimizer

        self.max_len = 256
        self.device = "cpu"
        self.finetune_batch_size = 32
    
    def load(self, checkpoint_path):
        checkpoint: dict=torch.load(checkpoint_path)
        model_state_dict = checkpoint.get("model_state_dict")
        optimizer_state_dict = checkpoint.get("optimizer_state_dict", self.optimizer.state_dict())
        self.model.load_state_dict(model_state_dict)
        self.optimizer.load_state_dict(optimizer_state_dict)

    def finetune(self, texts: np.array, sentiments: np.array):
        finetune_data = RobertaTrainSentimentData(texts, sentiments, self.tokenizer, self.max_len)
        train_params = {'batch_size': self.finetune_batch_size,
                        'shuffle': True,
                        'num_workers': 0
                        }
        finetune_loader = DataLoader(finetune_data, **train_params)
        finetune = RobertaFinetune(self.model, self.optimizer, self.loss_function)
        self.model = finetune.finetune(finetune_loader,self.device)

    def validate(self, texts: np.array, sentiments: np.array) -> float:
        validate_data = RobertaTrainSentimentData(texts, sentiments, self.tokenizer, self.max_len)
        validate_params = {'batch_size': self.finetune_batch_size,
                        'shuffle': True,
                        'num_workers': 0
                        }
        validation_loader = DataLoader(validate_data, **validate_params) 
        validate = RobertaValidate(self.model, self.loss_function)
        validation_loss = validate.validate(validation_loader, self.device)
        return validation_loss
    
    def infer(self, text: str):
        inference = RobertaInference(self.model, self.tokenizer, self.max_len, self.device)
        result = inference.infer(text)

        sentiment = "Undifined"
        if result ==0:
            sentiment = "Negative"
        elif result == 1:
            sentiment = "Neutral"
        elif result == 2:
            sentiment = "Positive"
        return sentiment

    def save(self, file_path):
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }
        torch.save(checkpoint, file_path)
