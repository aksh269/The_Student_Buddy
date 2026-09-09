import argparse
import json

from rag import chat


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the UniAsist RAG pipeline for a single user query."
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="The user query to send to the RAG pipeline.",
    )
    args = parser.parse_args()

    if args.query:
        user_query = args.query
    else:
        user_query = input("Enter your query: ").strip()

    if not user_query:
        raise SystemExit("No query provided.")

    response = chat(user_query, rerank=True)
    print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
