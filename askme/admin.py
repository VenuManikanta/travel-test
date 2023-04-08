from django.contrib import admin
from .models import Queries, Data, Food, Statistics, Search_history

# Register your models here.
# admin.site.register(model_name)

admin.site.register(Queries)
admin.site.register(Data)
admin.site.register(Food)
admin.site.register(Statistics)
# admin.site.register(Searches)
admin.site.register(Search_history)
