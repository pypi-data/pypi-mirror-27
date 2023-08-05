import services


class ReleaseNoteGenerator(object):
    DEFAULT_URL = 'https://github.counsyl.com/api/graphql'

    def __init__(self,
                 token,
                 client=services.GraphQLClient,
                 url=DEFAULT_URL,
                 repository_name='auto_pipeline',
                 release_fetcher=services.LatestReleaseFetcher,
                 pr_number_parser=services.PRNumberParser,
                 pr_fetcher=services.PRFetcher,
                 notes_parser=services.ReleaseNotesParser):

        self.client = client(url)
        self.client.inject_token(token)
        self.url = url
        self.token = token
        self.repository_name = repository_name
        self.release_fetcher = release_fetcher(
                                self.client,
                                repository_name=self.repository_name)
        self.pr_number_parser = pr_number_parser
        self.pr_fetcher = pr_fetcher(self.client)
        self.notes_parser = notes_parser

    def release_notes(self):
        release = self.release_fetcher.latest_release()
        pr_nums = self.pr_number_parser.parse_pr_numbers(release)
        pr_descriptions = self.pr_fetcher.fetch_pr_descriptions(
                            pr_nums, repository_name=self.repository_name)
        return self.notes_parser(pr_descriptions).parse_release_notes()
