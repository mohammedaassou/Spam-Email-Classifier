

import uvicorn

from spam_filter.api.main import app

def main() -> None:
    uvicorn.run(
        app = app
    )

