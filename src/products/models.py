import uuid
from datetime import datetime

from django.db import models
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
# Create your models here.

class ProductsBaseModel(DjangoCassandraModel):
    """
    Base model for all products.
    """
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    asin = columns.Text(required=True)
    created_at = columns.DateTime(default=datetime.now)
    

    # class Meta:
    #     db_table = 'products'
    #     ordering = ['name']  # Default ordering by name