from src.ingestion.loader import RepositoryLoader
from src.ingestion.exporter import DocumentExporter


def main():

    repo_path = "repo"

    loader = RepositoryLoader(repo_path)

    documents = loader.load()

    print(
        f"Loaded {len(documents)} files"
    )

    DocumentExporter.save(
        documents,
        "data/raw/repository.json"
    )

    print(
        "Saved repository metadata"
    )


if __name__ == "__main__":
    main()