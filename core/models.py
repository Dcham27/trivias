import string

from django.db import models
from django.urls import reverse
from django.conf import settings

from core.managers import CustomManagerAvowal

from hashids import Hashids

# Create your models here.
class HashidIdentifier:
    @staticmethod
    def _instance_hashid():
        return Hashids(
            salt=settings.SALT_HASHIDS,
            min_length=settings.MIN_LENGTH_HASHIDS,
            alphabet=string.ascii_lowercase,
        )

    @classmethod
    def public_identifier_encode(cls, *, pk):
        hashid = cls._instance_hashid()
        return hashid.encode(pk)

    @classmethod
    def public_identifier_decode(cls, *, code):
        hashid = cls._instance_hashid()
        return hashid.decode(code)


class Avowal(models.Model, HashidIdentifier):
    ACADEMIC = "academic"
    JOB = "job"
    FAMILY = "family"
    LOVE = "love"
    SEX = "sex"
    PERSONAL = "personal"
    POLITICS = "politics"
    TYPES = [
        (ACADEMIC, "🎓  - Academic"),
        (JOB, "💼  - Job"),
        (FAMILY, "🤲  - Family"),
        (LOVE, "❤️  - Love"),
        (SEX, "🔥  - Sex"),
        (PERSONAL, "⚱️  - Personal"),
        (POLITICS, "🌎  - Politics"),
    ]
    type_topic = models.CharField(max_length=8, choices=TYPES, default=ACADEMIC)
    public_identifier = models.CharField(max_length=50, blank=True, db_index=True)
    body = models.CharField(max_length=240)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomManagerAvowal.as_manager()

    def __str__(self):
        return self.public_identifier

    class Meta:
        app_label = "core"

    def get_absolute_url(self):
        return reverse("core:detail", kwargs={"code": self.public_identifier})

    @property
    def get_color_style(self):
        options = {
            "academic": "border-l-blue-600 bg-blue-300",
            "job": "border-l-slate-600 bg-slate-300",
            "family": "border-l-green-600 bg-green-300",
            "love": "border-l-pink-600 bg-pink-300",
            "sex": "border-l-red-600 bg-red-300",
            "personal": "border-l-yellow-600 bg-yellow-300",
            "politics": "border-l-orange-600 bg-orange-300",
        }
        return options.get(self.type_topic)

    @property
    def get_icon(self):
        options = {
            "academic": "🎓",
            "job": "💼",
            "family": "🤲",
            "love": "❤️",
            "sex": "🔥",
            "personal": "⚱️",
            "politics": "🌎",
        }
        return options.get(self.type_topic)


class Comment(models.Model, HashidIdentifier):
    avowal = models.ForeignKey(
        Avowal, related_name="comments", on_delete=models.CASCADE
    )
    body = models.CharField(max_length=120)
    public_identifier = models.CharField(max_length=50, blank=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.public_identifier
