from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin

from core.models import Avowal
from core.forms import CreateAvowal, CreateCommentForm
from cache.redis import get_cache_key, get_instance_from_cache, set_cache_instance


# Create your views here.
def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


class CreateAvowalView(CreateView):
    form_class = CreateAvowal
    template_name = "create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "title"
        ] = f"Create Avowals, statements, expressions, confessions, feelings, facts - Trivias"
        context[
            "description"
        ] = "Statements, expressions, confessions, feelings, facts, avowals, all about politics, sex, love, jobs and more, without restrictions."
        return context


class ListAvowalView(ListView):
    model = Avowal
    paginate_by = 12
    ordering = ("-id",)
    template_name = "home.html"
    context_object_name = "avowals"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Avowals about politics, love, sex and more - Trivias"
        context[
            "description"
        ] = "Statements, expressions, confessions, feelings, facts, avowals, all about politics, sex, love, jobs and more, without restrictions."
        return context

    def get_queryset(self):
        ordering = self.get_ordering()
        queryset = self.model.objects.filter(is_active=True).order_by(*ordering)
        return queryset


class DetailAvowalView(FormMixin, DetailView):
    model = Avowal
    pk_url_kwarg = "code"
    template_name = "detail.html"
    context_object_name = "avowal"
    form_class = CreateCommentForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if form.instance.is_active:
            form.instance.avowal_id = self.get_pk()
            form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCommentForm()
        context["error"] = kwargs.get("form")
        instance = self.object

        if instance:
            context[
                "title"
            ] = f"Avowal about {instance.type_topic} #{instance.public_identifier}"
            context["description"] = instance.body[:150]
        return context

    def get_success_url(self):
        return reverse(
            "core:detail",
            kwargs={
                "code": self.object.public_identifier,
            },
        )

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        try:
            obj = queryset
        except (
            queryset.model.DoesNotExist,
            queryset.model.MultipleObjectsReturned,
            Exception,
        ):
            raise Http404()
        return obj

    def get_queryset(self):
        pk = self.get_pk()
        cache_key = get_cache_key(pk)
        cache_data = get_instance_from_cache(cache_key)
        if cache_data:
            return cache_data
        queryset = self.model.objects.with_comments(pk)
        set_cache_instance(cache_key, queryset, 60)
        return queryset

    def get_pk(self):
        code = self.kwargs.get(self.pk_url_kwarg)
        pk = self.model.public_identifier_decode(code=code)
        try:
            pk = pk[0]
        except IndexError:
            return None
        return pk


class TopicFilterListView(ListView):
    model = Avowal
    paginate_by = 12
    ordering = ("id",)
    template_name = "home.html"
    context_object_name = "avowals"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("tag")
        context["title"] = f"Avowals about {self.kwargs.get('tag')} and more - Trivias"
        context[
            "description"
        ] = "Statements, expressions, confessions, feelings, facts, avowals, all about politics, sex, love, jobs and more, without restrictions."
        return context

    def get_queryset(self):
        ordering = self.get_ordering()
        topic = self.kwargs.get("tag")
        queryset = self.model.objects.filter(
            is_active=True, type_topic__iexact=topic
        ).order_by(*ordering)
        return queryset


class PrivacyView(TemplateView):
    template_name = "privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Privacy police - Trivias"
        context[
            "description"
        ] = "Statements, expressions, confessions, feelings, facts, avowals, all about politics, sex, love, jobs and more, without restrictions."
        return context
