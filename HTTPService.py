from fastapi import FastAPI
import uvicorn
import logging
from typing import Dict
from configparser import ConfigParser

class HTTPService:
   def __init__(self):
       self.app = FastAPI()
       self.config = ConfigParser()
       self.config.read('application.conf')
       self.logger = logging.getLogger(__name__)
       
       # Add routes
       self.setup_routes()

   def setup_routes(self):
       # Define routes here
       pass

def main():
   service = Service()
   
   config = service.config['http']
   host = config.get('interface', 'localhost')
   port = config.getint('port', 8080)

   uvicorn.run(
       service.app,
       host=host,
       port=port,
       log_level="info"
   )

if __name__ == "__main__":
   main()
