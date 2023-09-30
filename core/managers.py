from django.db import models


class CustomManagerAvowal(models.QuerySet):
    def with_comments(self, pk=None):
        if pk is not None:
            return self.filter(id=pk).prefetch_related("comments").first()
        return self.prefetch_related("comments")
