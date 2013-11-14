from scripts_helpers.corpora.dicts_builders.issues_corpora_builder import Builder as IssueCorporaBuilder
from scripts_helpers.corpora.dicts_builders.activities_corpora_builder import Builder as ActivityCorporaBuilder
import sys
from scripts_helpers.corpora.helper import Dictionary
from scripts_helpers.corpora.config_loader import ConfigReader
from scripts_helpers.corpora.redmine_services_provider import RedmineServicesProvider
import os

if __name__ == "__main__":

    os.chdir(sys.path[0])

    if len(sys.argv) == 1:
        conf_file = "../resources/config.cfg"
    else:
        conf_file = sys.argv[1]

    config_reader = ConfigReader(conf_file)
    service_provider = RedmineServicesProvider()

    issue_dictionary = Dictionary(config_reader, "from_issues", service_provider)
    IssueCorporaBuilder(config_reader, service_provider, issue_dictionary).generate_dicts()