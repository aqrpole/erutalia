# services/extractor/app/main.py
"""
Standalone Document Extractor CLI with Error Tracking
"""
import asyncio
import click
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from app.config import settings
from app.extract import DocumentProcessor
from app.embed import EmbeddingGenerator
from app.utils.logging import setup_logging

logger = setup_logging()

class ErrorTracker:
    def __init__(self, error_log_dir: str):
        self.error_log_dir = Path(error_log_dir)
        self.error_log_dir.mkdir(parents=True, exist_ok=True)
        self.error_log_file = self.error_log_dir / f"errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.failed_files = []

    def log_error(self, file_path: str, error: str, error_type: str = "processing"):
        """Log error to file and memory"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "error_type": error_type,
            "error_message": str(error)
        }

        self.failed_files.append(error_entry)

        # Append to error log file
        with open(self.error_log_file, 'a') as f:
            f.write(json.dumps(error_entry) + '\n')

        logger.error(f"Error logged for {file_path}: {error}")

    def get_summary(self):
        """Get error summary"""
        return {
            "total_failed": len(self.failed_files),
            "error_log_file": str(self.error_log_file),
            "failed_files": self.failed_files
        }

@click.group()
def cli():
    """University LLM Chatbot - Document Extractor"""
    pass

@cli.command()
@click.option('--input-dir', 
              default=settings.INPUT_DIR, 
              help='Directory containing documents to process')
@click.option('--collection', 
              default=settings.QDRANT_COLLECTION,
              help='Qdrant collection name')
@click.option('--chunk-size', 
              default=settings.CHUNK_SIZE,
              help='Text chunk size in characters')
@click.option('--batch-size', 
              default=settings.BATCH_SIZE,
              help='Batch size for embedding generation')
@click.option('--error-dir',
              default=settings.ERROR_LOG_DIR,
              help='Directory to store error logs')
def process(input_dir: str, collection: str, chunk_size: int, batch_size: int, error_dir: str):
    """Process all documents in directory and load into Qdrant"""
    # CHANGED: Direct function call instead of asyncio.run
    process_documents(input_dir, collection, chunk_size, batch_size, error_dir)

@cli.command()
@click.argument('file_path')
@click.option('--collection', 
              default=settings.QDRANT_COLLECTION,
              help='Qdrant collection name')
def process_file(file_path: str, collection: str):
    """Process a single file and load into Qdrant"""
    # CHANGED: Direct function call instead of asyncio.run
    process_single_file(file_path, collection)

@cli.command()
@click.option('--error-dir',
              default=settings.ERROR_LOG_DIR,
              help='Directory containing error logs')
def show_errors(error_dir: str):
    """Show recent processing errors"""
    display_recent_errors(error_dir)

@cli.command()
def health():
    """Check service health and connections"""
    check_health()

# CHANGED: Removed async
def process_documents(input_dir: str, collection: str, chunk_size: int, batch_size: int, error_dir: str):
    """Process all documents in directory with error tracking"""
    logger.info(f"Starting document processing from: {input_dir}")

    processor = DocumentProcessor()
    embedder = EmbeddingGenerator()
    error_tracker = ErrorTracker(error_dir)

    # Health check first
    logger.info("Performing health checks...")
    if not embedder.check_qdrant_health():
        logger.error("❌ Qdrant is not accessible. Please make sure it's running.")
        return

    if not embedder.check_embedding_health():
        logger.error("❌ Embedding model is not working.")
        return

    # Get all supported files
    files = processor.find_supported_files(input_dir)

    if not files:
        logger.warning(f"No supported files found in {input_dir}")
        return

    logger.info(f"Found {len(files)} files to process")

    successful = 0
    failed = 0

    for file_path in files:
        try:
            logger.info(f"Processing: {file_path}")

            # Extract and chunk text
            # CHANGED: Direct call instead of await
            chunks = processor.process_file(str(file_path), chunk_size)

            if not chunks:
                logger.warning(f"No content extracted from {file_path}")
                error_tracker.log_error(str(file_path), "No content extracted", "extraction")
                failed += 1
                continue

            # Generate embeddings and store in Qdrant
            metadata = {
                "collection": collection,
                "file_path": str(file_path),
                "batch_size": batch_size,
            }
            # CHANGED: Direct call instead of await
            success = embedder.process_chunks(chunks, metadata)

            if success:
                successful += 1
                logger.info(f"✅ Successfully processed {file_path} ({len(chunks)} chunks)")

                # Move to processed directory (optional)
                move_to_processed(file_path)
            else:
                failed += 1
                error_tracker.log_error(str(file_path), "Embedding/Qdrant storage failed", "storage")
                logger.error(f"❌ Failed to process {file_path}")

        except Exception as e:
            failed += 1
            error_tracker.log_error(str(file_path), str(e), "exception")
            logger.error(f"❌ Error processing {file_path}: {str(e)}")

    # Print summary
    logger.info("=" * 50)
    logger.info(f"PROCESSING SUMMARY:")
    logger.info(f"✅ Successful: {successful}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"📊 Success Rate: {(successful/len(files))*100:.1f}%")

    if failed > 0:
        error_summary = error_tracker.get_summary()
        logger.info(f"📝 Error log: {error_summary['error_log_file']}")
        logger.info(f"🔍 Run 'python -m app.main show-errors' to view detailed errors")

# CHANGED: Removed async
def process_single_file(file_path: str, collection: str):
    """Process a single file"""
    logger.info(f"Processing single file: {file_path}")

    processor = DocumentProcessor()
    embedder = EmbeddingGenerator()

    try:
        # CHANGED: Direct call instead of await
        chunks = processor.process_file(file_path, settings.CHUNK_SIZE)

        if not chunks:
            logger.warning(f"No content extracted from {file_path}")
            return

        # Generate embeddings and store in Qdrant
        metadata = {
            "collection": collection,
            "file_path": file_path,
            "batch_size": settings.BATCH_SIZE,
        }

        # CHANGED: Direct call instead of await
        success = embedder.process_chunks(chunks, metadata)

        if success:
            logger.info(f"✅ Successfully processed {file_path} ({len(chunks)} chunks)")
        else:
            logger.error(f"❌ Failed to process {file_path}")

    except Exception as e:
        logger.error(f"❌ Error processing {file_path}: {str(e)}")

# CHANGED: Removed async
def display_recent_errors(error_dir: str):
    """Display recent processing errors"""
    error_path = Path(error_dir)

    if not error_path.exists():
        logger.info("No error directory found")
        return

    # Find latest error file
    error_files = list(error_path.glob("errors_*.json"))
    if not error_files:
        logger.info("No error files found")
        return

    latest_file = max(error_files, key=os.path.getctime)

    logger.info(f"Recent errors from: {latest_file.name}")
    logger.info("=" * 50)

    with open(latest_file, 'r') as f:
        for line in f:
            error_data = json.loads(line.strip())
            print(f"📄 File: {error_data['file_path']}")
            print(f"⏰ Time: {error_data['timestamp']}")
            print(f"🚨 Error: {error_data['error_message']}")
            print(f"🔧 Type: {error_data['error_type']}")
            print("-" * 30)

# CHANGED: Removed async
def check_health():
    """Check service health"""
    logger.info("Performing health check...")

    embedder = EmbeddingGenerator()

    qdrant_healthy = embedder.check_qdrant_health()
    embedding_healthy = embedder.check_embedding_health()

    if qdrant_healthy and embedding_healthy:
        logger.info("✅ All services healthy")
    else:
        logger.error("❌ Some services are unhealthy")
        if not qdrant_healthy:
            logger.error("  - Qdrant connection failed")
        if not embedding_healthy:
            logger.error("  - Embedding service failed")

# CHANGED: Removed async
def move_to_processed(file_path: Path):
    """Move processed file to processed directory"""
    try:
        processed_dir = Path(settings.PROCESSED_DIR)
        processed_dir.mkdir(exist_ok=True)

        destination = processed_dir / file_path.name
        file_path.rename(destination)
        logger.debug(f"Moved {file_path} to processed directory")

    except Exception as e:
        logger.warning(f"Could not move file to processed directory: {str(e)}")

if __name__ == "__main__":
    cli()
