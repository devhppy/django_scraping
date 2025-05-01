import uuid
from datetime import datetime, timezone

from django.db import models
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from django_cassandra_engine.models import DjangoCassandraModel
# Create your models here.

class ProductsBaseModel(DjangoCassandraModel, Model):
    """
    Base model for all products.
    """
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    asin = columns.Text(primary_key=True, index=True)
    niche = columns.Text(required=True)
    affiliate_link = columns.Text()
    created_at = columns.DateTime(default=datetime.now(timezone.utc))
    

    class Meta:
        get_pk_field = 'asin'


class ScrapedProductDataModel(DjangoCassandraModel, Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    asin = columns.Text(index=True)
    title = columns.Text()
    price = columns.Float()
    total = columns.Float()
    description = columns.Text()
    image_url = columns.Text()
    rating = columns.Text()
    total_reviews = columns.Integer()
    # reviews = columns.List(columns.Text)
    updated_at = columns.DateTime(default=datetime.now(timezone.utc))

    class Meta:
        get_pk_field = 'id'