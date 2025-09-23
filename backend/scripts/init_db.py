"""
Database initialization script
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db

async def main():
    """Initialize the database"""
    print("Initializing database...")
    await init_db()
    print("Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(main())
