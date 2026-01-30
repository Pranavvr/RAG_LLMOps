from src.config.logging import setup_logging
from src.ingestion.fundamentals import build_company_cards_and_index

if __name__ == "__main__":
    
    setup_logging()
    build_company_cards_and_index(rebuild=True)
