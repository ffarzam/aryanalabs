from django_elasticsearch_dsl import Document,fields
from django_elasticsearch_dsl.registries import registry

from .models import Film,Critique


FILMS_SEARCH_FIELDS = {
    # api : database
    "name" : "name",
    "year" : "year",
    "genre" : "genre",
}

CRITIQUE_SEARCH_FIELDS = [
    "date__gte",
    "date__lte",
    "is_sploiler",
    "phrase",
]


@registry.register_document
class FilmDocument(Document):
    critique_set = fields.NestedField(
        properties = {
            "is_sploiler" : fields.BooleanField(),
            "date_submitted": fields.DateField(),
            "content": fields.TextField(),
        }
    )
    # critique_set = fields.NestedField(CritiqueDocument)


    class Django:
        model = Film
        fields = list(FILMS_SEARCH_FIELDS.values())
        related_models = [Critique]
        # ignore_signals = False


    class Index:
        name = "task"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Critique):
            return related_instance.film

    def update_document(self, instance, **kwargs):
        self.update(instance, **kwargs)
