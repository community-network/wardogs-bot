"""Run this to hot reload on changes"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=8081, reload=True)

# poetry run debug.py
