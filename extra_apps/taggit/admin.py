import xadmin
from taggit.models import Tag, TaggedItem


class TaggedItemInline(object):
    model = TaggedItem


class TagAdmin(object):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}

xadmin.site.register(Tag,TagAdmin)