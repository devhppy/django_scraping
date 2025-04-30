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
    asin = columns.Text(required=True, index=True)
    niche = columns.Text(required=True)
    affiliate_link = columns.Text()
    created_at = columns.DateTime(default=datetime.now(timezone.utc))
    

    # class Meta:
    #     db_table = 'products'
    #     ordering = ['name']  # Default ordering by name