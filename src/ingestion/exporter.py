import json
import os
from dataclasses import asdict


class DocumentExporter:

    @staticmethod
    def save(documents, output_path):

        # ✅ STEP 1: Ensure directory exists
        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        # Convert dataclasses → dict
        data = [
            asdict(doc)
            for doc in documents
        ]

        # Write file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)