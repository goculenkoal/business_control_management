import uvicorn
from loguru import logger

if __name__ == "__main__":
    logger.add(
        "utils/logs.json",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="10 MB",
        compression="zip",
        serialize=True,
    )

    uvicorn.run("src.main:app", port=8000, reload=True)
