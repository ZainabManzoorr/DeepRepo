import os

from src.config import (
    SUPPORTED_EXTENSIONS,
    IGNORED_DIRECTORIES,
)

from src.ingestion.document import Document


class RepositoryLoader:

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def load(self) -> list[Document]:

        documents = []

        for root, dirs, files in os.walk(self.repo_path):

            dirs[:] = [
                d
                for d in dirs
                if d not in IGNORED_DIRECTORIES
            ]

            for file in files:

                extension = os.path.splitext(file)[1]

                if extension not in SUPPORTED_EXTENSIONS:
                    continue

                full_path = os.path.join(root, file)

                try:

                    with open(
                        full_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    document = Document(
                        file=file,
                        path=full_path,
                        type=extension,
                        content=content
                    )

                    documents.append(document)

                except Exception as e:

                    print(
                        f"Error reading {full_path}: {e}"
                    )

        return documents