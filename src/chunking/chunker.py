import ast
from src.chunking.chunk import CodeChunk


class CodeChunker:

    def chunk_file(self, file_path: str, code: str):

        if file_path.endswith(".py"):
            return self.chunk_python_code(
                file_path,
                code
            )

        return self.fallback_chunk(
            file_path,
            code
        )

    def chunk_python_code(self, file_path: str, code: str):

        chunks = []

        try:
            tree = ast.parse(code)

        except SyntaxError:
            return self.fallback_chunk(
                file_path,
                code
            )

        lines = code.splitlines()

        for node in ast.walk(tree):

            # Function chunking
            if isinstance(node, ast.FunctionDef):

                start = node.lineno
                end = node.end_lineno or start

                chunk_text = "\n".join(
                    lines[start - 1:end]
                )

                chunks.append(
                    CodeChunk(
                        chunk=chunk_text,
                        file=file_path,
                        function=node.name
                    )
                )

            # Class chunking
            elif isinstance(node, ast.ClassDef):

                start = node.lineno
                end = node.end_lineno or start

                chunk_text = "\n".join(
                    lines[start - 1:end]
                )

                chunks.append(
                    CodeChunk(
                        chunk=chunk_text,
                        file=file_path,
                        class_name=node.name
                    )
                )

        if not chunks:
            return self.fallback_chunk(
                file_path,
                code
            )

        return chunks

    def fallback_chunk(
        self,
        file_path: str,
        code: str,
        chunk_size: int = 40
    ):

        lines = code.splitlines()

        chunks = []

        for i in range(
            0,
            len(lines),
            chunk_size
        ):

            chunk_text = "\n".join(
                lines[i:i + chunk_size]
            )

            chunks.append(
                CodeChunk(
                    chunk=chunk_text,
                    file=file_path
                )
            )

        return chunks