from fastapi import FastAPI
import asyncio
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import uvicorn
from src.utils.data_model import ServicenowData, DatabaseData
# Changing the order of following two imports leads to an error (dependency conflict) #check

from src.model.main import ModelProcess
from src.database.main import Database
from src.database.roberta_db import RobertaDB
from src.api.main import router
from src.preprocess.main import DataCleaner
from src.open_ai.main import APICall

@asynccontextmanager
async def lifespan(lifespan):
    print('app started...')
    schedular = BackgroundScheduler()

    # ---------------------- For testing ---------------------------------
    from datetime import datetime, timedelta
    time = datetime.now()+timedelta(seconds=15)
    hour = time.hour
    minute = time.minute
    second = time.second
    # --------------------------------------------------------------------

    schedular.add_job(func=inference_process, trigger="cron", hour=hour, minute=minute, second=second)
    schedular.add_job(func=finetune_process, trigger="cron", hour=hour, minute=minute+3, second=second)
    schedular.start()
    yield
    print("app stopped...")
    schedular.shutdown(wait=False)

def inference_process():
    process = multiprocessing.Process(target=inference)
    process.start()

def finetune_process():
    process = multiprocessing.Process(target=finetune)
    process.start()

def inference():
    '''Run periodically with following tasks:

    * Fetch comment from the service-now
    * Clean the data 
    * predict the sentiment by local model
    * Predict the sentiment by GPT
    * store the local model results in the database
    * store the GPT sentiment in the database
    '''
    # ----------------------------- the following part should be uncommented in actual setting ------------------------
    api = API()
    sn_data = ServicenowData()
    api.get_comments(sn_data)

    data_cleaner = DataCleaner()
    data_cleaner.clean(sn_data)

    model_process= ModelProcess()
    api_call = APICall()
    model_process.inference_process(sn_data)
    api_call.set_gpt_sentiments(sn_data)

    database = RobertaDB()
    database.insert_cases(sn_data)  # Insert Cases to the database.
    database.insert_gpt_sentiment(sn_data)  # Insert GPT sentiments to the database.

def finetune():
    database = RobertaDB()
    gpt_entries = database.get_gpt_entries()
    model_process = ModelProcess()
    model_process.finetune_process(gpt_entries)

app=FastAPI(lifespan=lifespan)
app.include_router(router)
if __name__ =="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
