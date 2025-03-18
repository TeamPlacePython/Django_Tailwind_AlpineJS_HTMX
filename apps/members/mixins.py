class HTMXMixin:

    def is_htmx_request(self):
        return self.request.headers.get("HX-Request") == "true"

    def get_htmx_template(self, htmx_template, default_template):
        return htmx_template if self.is_htmx_request() else default_template


class MemberQuerysetMixin:
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("sports_category")
            .prefetch_related("tags")
        )
