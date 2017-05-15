"""Module for constructing service deployment release notes using github api

Notes:
[1]  Github tags API only deals with tag objects - so only annotated tags, not
     lightweight tags.
[2]  set GITHUB_ACCESS_TOKEN as env variable or you'll be restricted to
     60 reqs/hour (vs. 5000)
"""

import os
import sys
import itertools
import requests
from six.moves import range
from output_helper import OutputHelper


HOST_GITHUB = 'github.com'
HOST_GITHUB_RAW = 'raw.githubusercontent.com'
MAX_COMPARISONS_TO_SHOW = 4
VERS = 0
SHA = 1
TYPE = 2
LINE = '------------------------------------'
CHANGELOG_NAMES = ['CHANGES', 'CHANGELOG', 'ChangeLog']
EXT = ['', '.rst', '.txt', '.RST', '.md']

CHANGELOG_FILENAMES = []
[CHANGELOG_FILENAMES.append(''.join(parts)) for parts in list(
    itertools.product(*[CHANGELOG_NAMES, EXT]))]

if os.environ['GITHUB_ACCESS_TOKEN']:
    ACCESS_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
else:
    ACCESS_TOKEN = ''


class NotFoundError(Exception):
    pass


class ReleaseNotes(object):
    """Used for GET operations against github API."""

    def __init__(self, repo_owner, repo, environment):

        self.output = OutputHelper()
        if all([repo_owner, repo, environment]):
            self._repo_owner = repo_owner
            self._repo = repo
            self._environment = environment.upper()
        else:
            exit('\nMissing github param\n\nABORTING!\n\n')

        self._url_github_api = self._get_url_github_api(
            HOST_GITHUB,
            repo_owner,
            repo
        )

        self._token_string = self._get_token_string(ACCESS_TOKEN)

        url = self._get_url_github_api_tags(
            self._url_github_api,
            self._token_string
        )

        req = self._get_tags(url)

        tags = req.json()
        self._max_comparisons = self._get_max_comparisons(tags)
        self._latest_tags = self._get_latest_tags(tags)
        self._last_tag = self._get_last_tag()
        self._last_tag_version = self._last_tag[VERS]

    @property
    def last_tag(self):
        return self._last_tag_version

    def _get_last_tag(self):
        """Return last tag"""

        return self._latest_tags[self._max_comparisons - 1]

    def _get_token_string(self, access_token):
        """Return access_token as url param (if exists)"""

        if access_token:
            return '?access_token={0}'.format(access_token)
        return ''

    def _get_url_github(self, host_github, repo_owner, repo):
        """Return github root URL as string"""

        return 'https://{0}/{1}/{2}'.format(
            host_github,
            repo_owner,
            repo
        )

    def _get_url_github_api(self, host_github, repo_owner, repo):
        """Return github API URL as string"""

        return 'https://api.{0}/repos/{1}/{2}/git'.format(
            host_github,
            repo_owner,
            repo
        )

    def _get_url_github_api_tags(self, url_github_api, token_string):

        return '{0}/refs/tags{1}'.format(
            url_github_api,
            token_string
        )

    def _get_url_changelog(self, url_github_raw, commit_sha, filename):

        return '{0}/{1}/{2}'.format(
            url_github_raw,
            commit_sha,
            filename
        )

    def _url_last_tag(self, url_github_api, last_tag_sha, token_string):

        return '{0}/tags/{1}{2}'.format(
            url_github_api,
            last_tag_sha,
            token_string
        )

    def _url_comparison(self, url_github, start, end):

        return '{0}/compare/{1}...{2}'.format(
            url_github,
            start,
            end
        )

    def _url_tag(self, url_github, tag_version):

        return '{0}/releases/tag/{1}'.format(url_github, tag_version)

    def _url_tag_commit(self, url_github, commit_sha):

        return '{0}/commit/{1}'.format(url_github, commit_sha)

    def _url_releases(self, url_github):

        return '{0}/releases'.format(url_github)

    def _get_max_comparisons(self, tags):
        """Calculates max comparisons to show

        Note:
            Display up to MAX_COMPARISONS_TO_SHOW (or less)

        Returns:
            integer - num of github release comparisons to display
        """

        count = len(tags)
        if count >= MAX_COMPARISONS_TO_SHOW:
            return MAX_COMPARISONS_TO_SHOW
        else:
            return count

    def _get_tags(self, url):
        """Get all tags as json from Github API."""

        req = requests.get(url)
        try:
            if 'Not Found' in req.text:
                raise NotFoundError
        except NotFoundError:
            err_header = self.output.get_header('ERROR')
            err_msg = '{0}\nNothing found at: \n{1}\nABORTING!\n\n'.format(
                err_header, url)
            sys.exit(err_msg)
        else:
            return req

    def _parse_tag(self, tag):
        """Parse a tag object for the data we want

        Return:
            list of desired elements
        """

        parts = tag['ref'].split('/')
        release_num = parts[2]
        sha = tag['object']['sha']
        type = tag['object']['type']
        url = tag['object']['url'] + self._token_string
        creation_date = self._get_commit_date(url)
        self.output.log((release_num, creation_date))
        return [release_num, sha, type, url, creation_date]

    def _get_latest_tags(self, tags):
        """Github API returns all tags indiscriminately, but
        we only want the latest.

        Return:
            list of lists containing:
        [release_num, sha, type, url, creation_date] for latest tags
        """

        self.output.log('Retrieve all tags', True)
        start = len(tags) - self._max_comparisons
        tags_unsorted = []

        for i in range(len(tags)):
            tag = self._parse_tag(tags[i])
            tags_unsorted.append(tag)

        self.output.log('Sort tags by commit date', True)
        tags_sorted = sorted(
            tags_unsorted, key=lambda tags_sorted: tags_sorted[4])
        self.output.log('DONE!')

        latest = []
        self.output.log('Get last tags from sorted list', True)
        for i in range(len(tags_sorted)):
            if i >= start:
                latest.append(tags_sorted[i])
                self.output.log(tags_sorted[i])
        self.output.log(latest)
        return latest

    def _get_commit_sha(self):
        """Return tag commit sha as string.

        Note:
            Varies depending on object type: type='tag' or 'commit'
            type='tag' requires a secondary call to retrieve commit url"""

        last_tag = self._last_tag
        if last_tag[TYPE] == 'tag':
            url = self._url_last_tag(
                self._url_github_api,
                last_tag[SHA],
                self._token_string
            )
            req = self._get_tags(url)
            return req.json()['object']['sha']
        else:
            return last_tag[SHA]

    def _get_commit_date(self, url):
        """Return tag or commit creation date as string."""

        req = self._get_tags(url)
        if 'git/tags' in url:
            return req.json()['tagger']['date'].split('T')[0]
        else:
            return req.json()['committer']['date'].split('T')[0]

    def _get_changelog(self, commit_sha):
        """"Parse and return CHANGELOG for latest tag as string"""

        url_github_raw = self._get_url_github(
            HOST_GITHUB_RAW, self._repo_owner, self._repo)

        for filename in CHANGELOG_FILENAMES:
            url = self._get_url_changelog(
                url_github_raw, commit_sha, filename)
            req = requests.get(url)
            try:
                if 'Not Found' in req.text:
                    raise NotFoundError
            except NotFoundError:
                pass
            else:
                break

        if req.text == 'Not Found':
            return ''

        lines = req.text

        # parse out release notes for this release only
        # only works if version numbers in changelog appear exactly
        # as they are tagged
        vers_latest = self._latest_tags[self._max_comparisons - 1][VERS]
        vers_previous = self._latest_tags[self._max_comparisons - 2][VERS]
        # print '---------'
        # print vers_latest
        # print vers_previous
        # print '---------'
        # exit()

        flag = False

        log = ''
        for line in lines.splitlines():
            if vers_latest in line:
                flag = True
            if vers_previous in line:
                flag = False
            if flag:
                log += line + '\n'

        # exit()
        return log

    def _get_section_release_notes(self, url_github):
        """Return bugzilla release notes with header as string"""

        notes = self.output.get_header('RELEASE NOTES')
        notes += self._url_releases(url_github) + '\n'
        return notes

    def _get_section_comparisons(self, url_github):
        """Return release notes - COMPARISONS section as string"""

        notes = self.output.get_sub_header('COMPARISONS')

        for i in range(0, self._max_comparisons - 1):
            start = self._latest_tags[i][VERS]
            end = self._latest_tags[i + 1][VERS]
            notes += self._url_comparison(url_github, start, end) + '\n'
        self.output.log('comparisons section - DONE!')
        return notes

    def _get_section_tags(self, url_github):
        """Return release notes - TAGS section as string"""

        commit_sha = self._get_commit_sha()
        notes = self.output.get_sub_header('TAGS')

        notes += self._url_tag(
            url_github,
            self._latest_tags[self._max_comparisons - 1][VERS]
        ) + '\n'
        notes += self._url_tag_commit(url_github, commit_sha) + '\n'

        notes += self._get_section_changelog(commit_sha)
        self.output.log('tags section - DONE!')
        return notes

    def _get_section_changelog(self, commit_sha):
        """Return release notes - CHANGELOG section as string"""

        changelog = self._get_changelog(commit_sha)
        self.output.log('changelog section - DONE!')
        if changelog:
            return self.output.get_sub_header('CHANGELOG') + changelog
        else:
            return ''

    def get_release_notes(self):
        """Return release notes for Bugzilla deployment ticket as string"""

        url_github = self._get_url_github(
            HOST_GITHUB,
            self._repo_owner,
            self._repo
        )

        self.output.log('Create release notes', True)
        notes = self._get_section_release_notes(url_github)
        notes += self._get_section_comparisons(url_github)
        notes += self._get_section_tags(url_github)
        return notes


def main():

    ReleaseNotes()


if __name__ == '__main__':
    main()
