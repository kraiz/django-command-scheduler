from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.formats import localize
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.translation import gettext
from command_scheduler.models import Command, Log


def kill_command(modeladmin, request, queryset):
    logs = list(command.last_log for command in queryset.all())
    for log in logs:
        log.kill()
kill_command.short_description = 'Kill the running command'


class CommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'enabled', 'parallel', 'status',
                    'last_execution', 'next_execution')
    actions = [kill_command]

    def status(self, obj):
        log = obj.last_log
        if log is None:
            icon = 'success'
            text = 'Scheduled'
        elif log.is_running():
            icon = 'clock'
            text = 'Running'
        elif log.success:
            icon = 'success'
            text = 'Successful'
        else:
            icon = 'alert'
            text = 'Error'

        return format_html(
            '<img src="/static/admin/img/icon_{0}.gif" width="12" height="12">'
            ' {1}',
            icon,
            text
        )
    status.allow_tags = True

    def last_execution(self, obj):
        return format_html(
            '{0} <a href="{1}?command__name__exact={2}" title="{3}">({3})</a>',
            localize(obj.last_execution),
            reverse('admin:command_scheduler_log_changelist'),
            obj.name,
            gettext('Logs')
        )
    last_execution.allow_tags = True


class LogAdmin(admin.ModelAdmin):
    list_display = ('command', 'pid', 'started', 'duration', 'success')
    list_filter = ('success', 'command__name')
    search_fields = ('command__name', 'pid', 'stdout', 'stderr')
    fields = ('command', 'pid', 'started', 'ended', 'success', 'stdout',
              'stderr')
    readonly_fields = fields
    date_hierarchy = 'started'

    class Media:
        css = {
            'all': ('command_scheduler.css',)
        }

    def duration(self, obj):
        if obj.ended is None:
            return '%s (still running)' % (now() - obj.started)
        else:
            return obj.ended - obj.started

admin.site.register(Command, CommandAdmin)
admin.site.register(Log, LogAdmin)