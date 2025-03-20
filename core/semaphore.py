import asyncio
import settings


semaphore = asyncio.Semaphore(settings.threads)