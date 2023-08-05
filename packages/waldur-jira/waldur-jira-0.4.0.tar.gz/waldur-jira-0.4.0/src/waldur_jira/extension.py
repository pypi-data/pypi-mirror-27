from __future__ import unicode_literals

from nodeconductor.core import NodeConductorExtension


class JiraExtension(NodeConductorExtension):

    class Settings:
        WALDUR_JIRA = {
            'COMMENT_TEMPLATE': '{body}\n\n_(added by {user.full_name} [{user.username}] via G-Cloud Portal)_',
            # Optional mapping of priority names in Waldur and JIRA
            'PRIORITY_MAPPING': {
                'Minor': '3 - Minor',
                'Major': '2 - Major',
                'Critical': '1 - Critical',
            }
        }

    @staticmethod
    def django_app():
        return 'waldur_jira'

    @staticmethod
    def django_urls():
        from .urls import urlpatterns
        return urlpatterns

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in
