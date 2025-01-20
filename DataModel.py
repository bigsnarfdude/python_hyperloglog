from dataclasses import dataclass
from datetime import datetime
from typing import List
import json

@dataclass
class Record:
   Date: str
   Ledger: str 
   Amount: str
   Company: str

@dataclass
class NormalizedRecord:
   Date: datetime
   Ledger: str
   Amount: float 
   Company: str

@dataclass
class PageRecords:
   totalCount: int
   page: int
   transactions: List[Record]

@dataclass
class Result:
   estimatedSize: float

@dataclass 
class Page:
   page: str

@dataclass
class AddHLL:
   key: str
   value: str

@dataclass
class HLLResult:
   key: str
   estimatedSize: float
   hllString: str

@dataclass
class GetHyperLogLog:
   servername: str
   count: str
   interval: str
   timestamp: str

@dataclass
class EstimatedSize:
   servername: str
   interval: str
   estimatedSize: float

def from_json(json_str: str, cls):
   return cls(**json.loads(json_str))

def to_json(obj):
   return json.dumps(obj.__dict__)
