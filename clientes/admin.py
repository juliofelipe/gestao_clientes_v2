from django.contrib import admin
from .models import Person, Document, Sales, Product


admin.site.register(Person)
admin.site.register(Document)
admin.site.register(Sales)
admin.site.register(Product)