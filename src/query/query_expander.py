class QueryExpander:

    EXPANSIONS = {
        "login": [
            "authentication",
            "signin",
            "user login"
        ],

        "jwt": [
            "token",
            "authentication",
            "bearer token"
        ],

        "database": [
            "db",
            "storage",
            "repository"
        ]
    }

    def expand(self, query):

        expanded = [query]

        words = query.lower().split()

        for word in words:

            if word in self.EXPANSIONS:

                expanded.extend(
                    self.EXPANSIONS[word]
                )

        return " ".join(expanded)