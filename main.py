from fastapi import FastAPI, Request, HTTPException
import logging
import os

# Ensure logs directory exists in the ROOT directory (not app/logs)
current_dir = os.path.dirname(os.path.abspath(_file_))
root_dir = os.path.dirname(current_dir)  # This goes up one level to the root
logs_dir = os.path.join(root_dir, "logs")
os.makedirs(logs_dir, exist_ok=True)

# Clear any existing logging configuration
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Setup logging to file in the ROOT logs directory
log_file_path = os.path.join(logs_dir, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=log_file_path,
    filemode="a"  # Append mode
)

# Also add console handler to see logs in terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

app = FastAPI(title="Library Management System", version="1.0.0")

# Middleware for automatic logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logging.info(f"Response: {response.status_code}")
    return response

@app.get("/")
def home():
    return {"message": "Library Management System"}

@app.get("/items")
def get_items():
    """Get all books from the library"""
    try:
        # Look for books.txt in app/data directory
        current_dir = os.path.dirname(os.path.abspath(_file_))
        file_path = os.path.join(current_dir, "data", "books.txt")
        
        logging.info(f"Looking for books file at: {file_path}")
        
        with open(file_path, "r") as file:
            content = file.read()
            
    except FileNotFoundError:
        logging.warning("Books file not found, returning default books")
        return ["The Great Gatsby", "To Kill a Mockingbird", "1984"]
        
    except Exception as e:
        logging.error(f"Error reading books file: {str(e)}")
        return ["Error loading books"]
    
    # Process the book data
    books_list = []
    for line in content.splitlines():
        book = line.strip()
        if book:
            books_list.append(book)
    
    logging.info(f"Returning {len(books_list)} books")
    return books_list

@app.get("/health")
def health_check():
    return {"status": "ok"}

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
