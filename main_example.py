import uvicorn
from fastapi import FastAPI
from Service import Service
from HLLService import HLLService
from HLLMonoid import HLLMonoid
from Generators import Generator
from datetime import datetime
from DateUtility import DateUtility

# Initialize services
app = FastAPI()
hll_service = HLLService(host="localhost", port=6379)
service = Service(redis_host="localhost", redis_port=6379)

def demo_hll_workflow():
    # Generate sample data
    print("Generating sample data...")
    random_numbers = Generator.random_numbers(10000, 1000)
    
    # Create HLL from integers
    print("Creating HLL from integers...")
    hll = HLLMonoid.load_list_int(random_numbers)
    
    # Get current timestamp bucket
    now = datetime.now()
    bucket = DateUtility.bucket(now)
    print(f"Current time bucket: {bucket}")
    
    # Store HLL in Redis
    key = f"demo_hll_{bucket}"
    serialized_hll = service.MAGIC + str(hll.count())
    success = hll_service.put(key, serialized_hll)
    print(f"Stored HLL in Redis with key {key}: {success}")
    
    # Retrieve and check cardinality
    retrieved = hll_service.get(key)
    if retrieved:
        print(f"Retrieved HLL count: {retrieved}")
        
    return {
        "original_count": len(set(random_numbers)),
        "hll_estimate": hll.count(),
        "stored_key": key
    }

if __name__ == "__main__":
    # Run the demo
    results = demo_hll_workflow()
    print("\nResults:", results)
    
    # Start the FastAPI service
    uvicorn.run(
        service.app,
        host="localhost",
        port=8080,
        log_level="info"
    )
