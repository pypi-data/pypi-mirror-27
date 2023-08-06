import copy

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy, gettext


def duplicate_model(modeladmin, request, instance, updated_data=None, first_level=False):
    """

    :type modeladmin admin.ModelAdmin
    :type request django.http.HttpRequest
    :type instance django.db.models.Model
    :type updated_data dict
    :return:
    """
    clone = copy.deepcopy(instance)
    clone.id = None

    if updated_data:
        for k, v in updated_data.items():
            setattr(clone, k, v)

    if hasattr(clone, 'pre_duplicate') and callable(clone.pre_duplicate):
        clone.pre_duplicate(instance, first_level)
    clone.save()

    options = clone._meta

    for relation_ref in options.many_to_many:
        relation_name = relation_ref.name
        relation = getattr(clone, relation_name)
        origin_relation = getattr(instance, relation_name)

        relation.set(origin_relation.all())

    for relation_ref in options.many_to_many:
        relation_name = relation_ref.name
        relation = getattr(clone, relation_name)
        origin_relation = getattr(instance, relation_name)

        relation.set(origin_relation.all())

    if modeladmin:
        inline_models = [inline.model for inline in modeladmin.inlines]

        for related_ref in options.related_objects:
            if related_ref.related_model in inline_models:
                related_name = related_ref.related_name
                if not related_name:
                    related_name = '{}_set'.format(related_ref.name)
                objects = getattr(instance, related_name).all()
                if admin.site.is_registered(related_ref.related_model):
                    model_modeladmin = admin.site._registry[related_ref.related_model]
                else:
                    model_modeladmin = None

                for obj in objects:
                    cloned_obj = duplicate_model(model_modeladmin, request, obj, {
                        related_ref.field.name: clone
                    })
                    cloned_obj.save()

    if hasattr(clone, 'post_duplicate') and callable(clone.post_duplicate):
        clone.post_duplicate(instance)
        clone.save()

    return clone


def duplicate_models(modeladmin, request, queryset):
    """

    :param modeladmin:
    :type modeladmin: admin.ModelAdmin
    :param request:
    :param queryset:
    :return:
    """
    if not modeladmin.has_add_permission(request):
        raise PermissionDenied

    for instance in queryset:
        duplicate_model(modeladmin, request, instance, first_level=True)

    messages.success(
        request,
        gettext('%(count)s %(verbose_name_plural)s have been duplicated') % {
            'count': len(queryset),  # looped already so this wont call another query
            'verbose_name_plural': modeladmin.model._meta.verbose_name_plural,
        }
    )


duplicate_models.short_description = gettext_lazy('Duplicate selected %(verbose_name_plural)s')


admin.site.add_action(duplicate_models)
