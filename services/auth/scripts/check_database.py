# services/auth-service/scripts/check_database.py
#!/usr/bin/env python3
"""
Database connection troubleshooting script
"""
import asyncio
import asyncpg
from app.core.config import settings

async def check_database_connection():
    print("🔍 Checking database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")

    try:
        # Extract connection details from URL
        # postgresql+asyncpg://user:pass@host:port/dbname
        url_parts = settings.DATABASE_URL.replace("postgresql+asyncpg://", "").split("@")
        auth_part = url_parts[0].split(":")
        host_part = url_parts[1].split("/")
        db_part = host_part[1].split(":")

        user = auth_part[0]
        password = auth_part[1] if len(auth_part) > 1 else ""
        host = host_part[0].split(":")[0]
        port = host_part[0].split(":")[1] if ":" in host_part[0] else "5432"
        database = db_part[0]

        print(f"Connecting to: {host}:{port}/{database} as user: {user}")

        # Test connection
        conn = await asyncpg.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )

        print("✅ Database connection successful!")

        # Check if database exists and is accessible
        version = await conn.fetchval("SELECT version();")
        print(f"PostgreSQL version: {version}")

        # Check if our tables exist
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)

        print(f"Found {len(tables)} tables in database")
        for table in tables:
            print(f"  - {table['table_name']}")

        await conn.close()

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if PostgreSQL is running: sudo systemctl status postgresql")
        print("2. Check PostgreSQL logs: sudo tail -f /var/log/postgresql/postgresql-*.log")
        print("3. Verify connection details in .env file")
        print("4. Test connection manually: psql -h host -U user -d database")

if __name__ == "__main__":
    asyncio.run(check_database_connection())
