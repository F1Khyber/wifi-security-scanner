from config.database import (
    test_connection,
    ensure_collection
)

from ai.vector_search import create_vector_index


if __name__ == "__main__":

    test_connection()

    ensure_collection()

    create_vector_index()