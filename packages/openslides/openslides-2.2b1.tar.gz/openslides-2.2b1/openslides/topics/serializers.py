from openslides.utils.rest_api import ModelSerializer
from openslides.utils.validate import validate_html

from .models import Topic


class TopicSerializer(ModelSerializer):
    """
    Serializer for core.models.Topic objects.
    """
    class Meta:
        model = Topic
        fields = ('id', 'title', 'text', 'attachments', 'agenda_item_id')

    def validate(self, data):
        if 'text' in data:
            data['text'] = validate_html(data['text'])
        return data
