from typing import Optional, List
from datetime import datetime
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import redis
from datasketch import HyperLogLog

class PageRecords(BaseModel):
   total_count: int
   transactions: List[dict]

class NormalizedRecord(BaseModel):
   date: datetime
   ledger: str
   amount: float
   company: str

class Page(BaseModel):
   page: str

class AddHLL(BaseModel):
   key: str

class Result(BaseModel):
   value: float

class HLLResult(BaseModel):
   key: str
   count: int
   hll_string: str

class Service:
   def __init__(self, redis_host="localhost", redis_port=6379):
       self.app = FastAPI()
       self.redis_client = redis.Redis(host=redis_host, port=redis_port)
       self.MAGIC = "%%%"
       self.items_per_page = 10
       self.setup_routes()

   async def fetch_mock_info(self, page: str) -> dict:
       async with httpx.AsyncClient() as client:
           response = await client.get(f"http://127.0.0.1:8000/transactions/{page}")
           if response.status_code == 200:
               return response.json()
           raise HTTPException(status_code=response.status_code)

   def to_cleaned_record(self, result: dict) -> NormalizedRecord:
       company = result["Company"].strip(''.join(c for c in result["Company"] if not c.isalnum() and c not in " /.")).split("x")[0].strip()
       return NormalizedRecord(
           date=datetime.strptime(result["Date"], "%Y-%m-%d"),
           ledger=result["Ledger"],
           amount=float(result["Amount"]),
           company=company
       )

   async def get_total_count(self, page: str) -> int:
       data = await self.fetch_mock_info(page)
       return data["total_count"] // self.items_per_page + 1

   async def get_group(self, query: str) -> List[NormalizedRecord]:
       data = await self.fetch_mock_info(query)
       return [self.to_cleaned_record(t) for t in data["transactions"]]

   async def de_duped(self, page: str) -> float:
       end = await self.get_total_count(page)
       start = int(page.split('.')[0])
       records = []
       for i in range(start, end + 1):
           group = await self.get_group(page)
           records.extend(group)
       return sum(set(r.amount for r in records))

   def add_hll_redis(self, hll_update: AddHLL) -> HLLResult:
       numbers = Generator.one_million_random_numbers()
       hll = HLLMonoid.load_list_int(numbers)
       count = len(hll)
       hll_string = HLLSerializer.to_magic_string(hll)
       now = datetime.now()
       keyed = f"{hll_update.key}_{DateUtility.bucket(now)}"
       success = HLLService.put(keyed, hll_string)
       return HLLResult(key=keyed, count=count, hll_string=hll_string)

   def get_hll_estimated_size(self, hll_get: AddHLL) -> Result:
       key = hll_get.key
       keyed = HLLService.get(key)
       if keyed:
           hydrated_hll = HLLSerializer.from_magic_string(keyed)
           return Result(value=len(hydrated_hll))
       raise HTTPException(status_code=404)

   def get_distinct(self, key: str) -> Result:
       keyed = HLLService.get(key)
       if keyed:
           hydrated_hll = HLLSerializer.from_magic_string(keyed)
           return Result(value=len(hydrated_hll))
       raise HTTPException(status_code=404)

   def setup_routes(self):
       @self.app.post("/totalBalanceDeDuped")
       async def total_balance_de_duped(page: Page):
           return Result(value=await self.de_duped(page.page))

       @self.app.post("/getHLL")
       def get_hll(hll_get: AddHLL):
           return self.get_hll_estimated_size(hll_get)

       @self.app.post("/addHLL") 
       def add_hll(hll_update: AddHLL):
           return self.add_hll_redis(hll_update)

       @self.app.get("/distinct/{server_name}")
       def distinct(server_name: str):
           return self.get_distinct(server_name)
