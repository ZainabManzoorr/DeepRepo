import re


class MetadataFilter:

    def __init__(self):
        pass

    # -------------------------
    # Extract File Name
    # -------------------------
    def extract_file(
        self,
        query: str
    ):

        match = re.search(
            r"[\w\-]+\.(py|js|ts|jsx|tsx|java|cpp|c|go|rs)",
            query.lower()
        )

        if match:
            return match.group(0)

        return None

    # -------------------------
    # Extract Function Name
    # -------------------------
    def extract_function(
        self,
        query: str
    ):

        patterns = [
            r"function\s+(\w+)",
            r"method\s+(\w+)",
            r"explain\s+(\w+)",
            r"what does\s+(\w+)\s+do"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                query.lower()
            )

            if match:

                candidate = match.group(1)

                if "." not in candidate:
                    return candidate

        return None

    # -------------------------
    # Detect Filters
    # -------------------------
    def resolve_file_filter(self, filters, symbol_table):
       """
      Convert function-based query into real file mapping
      """

       if "file" in filters:

         file_query = filters["file"]
         
         files = {
             info['file']
             for info in symbol_table.all_symbols().values()
         }

        # if user asked login.py but it doesn't exist
       if not any(path.endswith(requested) for path in files):

          candidate = file_query.replace(".py", "")

          resolved = symbol_table.resolve_function_file(candidate)

       if resolved:
            filters.pop("file")
            filters["function"] = candidate

       return filters

    # -------------------------
    # Apply Filter
    # -------------------------
    def apply(
        self,
        chunks,
        filters
    ):

        if not filters:
            return chunks

        filtered = []

        for chunk in chunks:

            keep = True

            # File filter
            if "file" in filters:

                if filters["file"] not in (
                    chunk.get(
                        "file",
                        ""
                    ).lower()
                ):
                    keep = False

            # Function filter
            if (
                keep
                and
                "function" in filters
            ):

                if filters["function"] != (
                    chunk.get(
                        "function",
                        ""
                    ).lower()
                ):
                    keep = False

            if keep:
                filtered.append(
                    chunk
                )

        return filtered