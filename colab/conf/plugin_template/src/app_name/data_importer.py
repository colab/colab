
from colab.plugins.data import PluginDataImporter


class {{ app_name_camel }}DataImporter(PluginDataImporter):
    app_label = '{{ app_name }}'

    def fetch_data(self):
        pass
