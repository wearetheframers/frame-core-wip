import asyncio
import tracemalloc
from .cli import main

if __name__ == "__main__":
    tracemalloc.start()
    asyncio.run(main())
