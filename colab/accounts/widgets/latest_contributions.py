from colab.widgets.widget_manager import Widget
from colab.plugins.utils.collaborations import get_collaboration_data


class LatestContributionsWidget(Widget):
    name = 'latest contributionsp'
    template = 'widgets/latest_contributions.html'

    def generate_content(self, **kwargs):
        collaborations, count_types_extras = get_collaboration_data(
            kwargs['context']['user'], kwargs['context']['object'].username)

        collaborations.sort(key=lambda elem: elem.modified, reverse=True)
        kwargs['context']['results'] = collaborations[:10]

        super(LatestContributionsWidget, self).generate_content(**kwargs)
