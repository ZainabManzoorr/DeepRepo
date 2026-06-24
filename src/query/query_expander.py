class QueryExpander:

    EXPANSIONS = {

    "authentication": [
        "login",
        "signin",
        "credential verification",
        "password check",
        "user authentication"
    ],

    "login": [
        "authentication",
        "signin",
        "user login"
    ],

    "jwt": [
        "token",
        "bearer token",
        "authentication"
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