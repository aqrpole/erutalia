# services/auth-service/app/core/database.py
import logging
import asyncio
from sqlalchemy             import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm         import sessionmaker
from sqlalchemy.orm         import declarative_base
from sqlalchemy.exc         import SQLAlchemyError, OperationalError
from asyncpg.exceptions     import ConnectionDoesNotExistError, CannotConnectNowError
from core.config            import settings

logger            = logging.getLogger(__name__)

# Database engine
engine            = None
AsyncSessionLocal = None
Base              = declarative_base()

async def get_db():
    """Dependency for getting database session"""
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db(max_retries: int = 3, retry_delay: int = 5):
    """Initialize database connection and create tables with retry logic"""
    global engine, AsyncSessionLocal

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{max_retries})...")

            # Create engine
            engine = create_async_engine(
                settings.DATABASE_URL,
                pool_size=settings.DATABASE_POOL_SIZE,
                max_overflow=settings.DATABASE_MAX_OVERFLOW,
                echo=settings.DEBUG,
                pool_pre_ping=True  # Check connection before using
            )

            # Session factory
            AsyncSessionLocal = sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

            # Test connection
            async with engine.begin() as conn:
                await conn.run_sync(lambda sync_conn: sync_conn.execute (text ("SELECT 1")))

            logger.info("✅ Database connection established")

            # Create tables
            await create_tables()

            logger.info("✅ Database initialization completed successfully")
            return True

        except OperationalError as e:
            logger.error(f"❌ Database operational error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                continue
            else:
                logger.critical("❌ Failed to connect to database after all retry attempts")
                await handle_database_failure()
                return False

        except ConnectionDoesNotExistError as e:
            logger.error(f"❌ Database connection does not exist (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                continue
            else:
                logger.critical("❌ Database connection failed permanently")
                await handle_database_failure()
                return False

        except CannotConnectNowError as e:
            logger.error(f"❌ Cannot connect to database now (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                continue
            else:
                logger.critical("❌ Database connection refused permanently")
                await handle_database_failure()
                return False

        except SQLAlchemyError as e:
            logger.error(f"❌ SQLAlchemy error during initialization: {e}")
            await handle_database_failure()
            return False

        except Exception as e:
            logger.error(f"❌ Unexpected error during database initialization: {e}")
            await handle_database_failure()
            return False

async def create_tables ():
    """Create database tables"""
    try:
        # Import all models here to ensure they are registered with Base
        from models.user import User, RefreshToken

        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info ("✅ Database tables created successfully")

    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise

async def handle_database_failure():
    """Handle database connection failure gracefully"""
    logger.error("Handling database connection failure...")

    # Close any existing connections
    await close_db()

    # Log detailed error information for debugging
    logger.error("Database connection failed. Please check:")
    logger.error("1. Is PostgreSQL running?")
    logger.error("2. Check DATABASE_URL in .env file")
    logger.error(f"3. Current DATABASE_URL: {settings.DATABASE_URL}")
    logger.error("4. Check PostgreSQL logs for errors")

    # You could also send alert/notification here
    # await send_alert_notification("Database connection failed")

async def close_db():
    """Close database connection gracefully"""
    global engine
    if engine:
        try:
            await engine.dispose()
            logger.info("✅ Database connection closed gracefully")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
        finally:
            engine = None

async def check_database_health() -> bool:
    """Check if database is healthy"""
    if not engine:
        logger.error("Database engine not initialized")
        return False

    try:
        async with engine.begin () as conn:
            await conn.run_sync (lambda sync_conn: sync_conn.execute( text("SELECT 1")))
        logger.debug("✅ Database health check passed")
        return True
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return False
