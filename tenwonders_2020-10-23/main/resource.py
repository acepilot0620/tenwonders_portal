from import_export import resources
from .models import Influencer_DB

class InfluencerResource(resources.ModelResource):
    class Meta:
        model = Influencer_DB