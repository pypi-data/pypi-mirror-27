# coding=utf-8
import logging

from django.contrib import admin

from .models import RemoteExperiment


_all__ = (
    'RemoteExperimentAdmin',
)


logger = logging.getLogger(__file__)


@admin.register(RemoteExperiment)
class RemoteExperimentAdmin(admin.ModelAdmin):
    list_display = (
        'admin_link',
        'site',
        'state',
        'start_date',
        'end_date',
        'participants',
        'confidences',
    )
    list_display_links = None
    list_filter = (
        'site',
        'state',
    )
    search_fields = (
        'name',
    )

    def admin_link(self, obj):
        return '<a href="{admin_url}" target="_blank">{name}</a>'.format(
            admin_url=obj.admin_url,
            name=obj.name,
        )
    admin_link.short_description = 'name'
    admin_link.allow_tags = True
    admin_link.admin_order_field = 'name'

    def participants(self, obj):
        return sum(dict(obj.statistics['alternatives']).values())

    def confidences(self, obj):
        if not obj.alternatives_list:
            return 'no alternatives'
        primary_alternatives = list(filter(
            lambda alt: alt['is_primary'],
            obj.statistics['results'].values())
        )
        if not primary_alternatives:
            return 'no primary goals'

        def _td(data):
            confidence = data['confidence']
            value = '{0:.2f}%'.format(confidence) if confidence else 'N/A'
            return '<td>{}</td>'.format(value)

        def _goal(name, data):
            data_dict = dict(data['alternatives'])
            data_html = ''.join(
                _td(data_dict[alternative])
                for alternative in obj.alternatives_list
                if alternative != 'control')
            return '<tr><th scope="row">{goal}</th>{data_html}</tr>'.format(
                goal=name,
                data_html=data_html,
            )

        alterantives_header_html = ''.join(
            '<th>{}</th>'.format(alternative)
            for alternative in obj.alternatives_list
            if alternative != 'control'
        )
        table_html = (
            '<table class="ministats">'
            '<tr><td></td>{alterantives_header_html}</tr>'
            '{goals}'
            '</table>')
        results = obj.statistics['results']
        goals_html = '\n'.join(
            _goal(goal, results[goal])
            for goal in sorted(results)
            if results[goal]['is_primary']
        )
        return table_html.format(
            alterantives_header_html=alterantives_header_html,
            goals=goals_html,
        )
    confidences.allow_tags = True
    confidences.short_description = 'confidence intervals'

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(RemoteExperimentAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def changelist_view(self, request, extra_context=None):
        excs = RemoteExperiment.update_remotes()
        for e in excs:
            self.message_user(
                request, 'Error updating from {site}: {e}'.format(
                    site=e.server['url'],
                    e=repr(e.original_exception),
                ))
        return super(RemoteExperimentAdmin, self).changelist_view(
            request, extra_context)
