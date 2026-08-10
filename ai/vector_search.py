from datetime import datetime, timezone

from pymongo.operations import SearchIndexModel

from config.database import security_events


VECTOR_INDEX_NAME = "security_event_vector_index"


def create_vector_index():
    """
    Create the MongoDB Vector Search index.

    all-MiniLM-L6-v2 produces 384-dimensional vectors.
    """

    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 384,
                    "similarity": "cosine"
                }
            ]
        },
        name=VECTOR_INDEX_NAME,
        type="vectorSearch"
    )

    security_events.create_search_index(
        model=search_index_model
    )

    print(
        f"Vector Search index '{VECTOR_INDEX_NAME}' "
        "creation requested."
    )


def store_security_event(
    network,
    event_text,
    embedding,
    alerts=None
):
    """
    Store a WiFi security event and its embedding.
    """

    document = {
        "ssid": network.get("ssid"),
        "bssid": network.get("bssid"),
        "authentication": network.get("authentication"),
        "encryption": network.get("encryption"),
        "signal": network.get("signal"),
        "channel": network.get("channel"),

        "event_text": event_text,

        "alerts": alerts or [],

        "embedding": embedding,

        "created_at": datetime.now(timezone.utc)
    }

    result = security_events.insert_one(document)

    return str(result.inserted_id)


def search_similar_events(
    query_embedding,
    limit=5,
    num_candidates=100
):
    """
    Find security events similar to the supplied embedding.
    """

    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": num_candidates,
                "limit": limit
            }
        },
        {
            "$project": {
                "_id": 0,
                "ssid": 1,
                "bssid": 1,
                "authentication": 1,
                "encryption": 1,
                "signal": 1,
                "channel": 1,
                "event_text": 1,
                "alerts": 1,
                "created_at": 1,

                "similarity_score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }
    ]

    results = security_events.aggregate(pipeline)

    return list(results)