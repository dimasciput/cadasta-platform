from core.views.generic import TemplateView
from core.mixins import LoginPermissionRequiredMixin
from organization import messages as org_messages
from .mixins import SearchResultsMixin


class Search(LoginPermissionRequiredMixin,
             SearchResultsMixin,
             TemplateView):
    template_name = 'search/search.html'
    permission_required = 'project.view_private'
    permission_denied_message = org_messages.PROJ_VIEW

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['search_results'] = self._format_search_results()
        return context

    def get_object(self, queryset=None):
        return self.get_project()

    def get_perms_objects(self):
        return [self.get_project()]
