#!/usr/bin/python3

import os
import argparse
import config
import git
import shutil
import arrow
import html
import re


class Mbs(object):

    def __init__(self, repository=None, destination=None, sources_pull=True):
        self.repository = repository if repository else config.REPOSITORY_URL
        self.destination = os.path.join(destination if destination else config.DESTINATION)
        self.sources_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sources')
        self.sources_pull = sources_pull
        self.date = arrow.now().format('YYYY-MM-DD_HH-mm')
        self.files_path = os.path.join(self.destination, self.date)
        self.txt_path = os.path.join(self.files_path, 'sources.txt')
        self.html_path = os.path.join(self.files_path, 'sources.html')

        shutil.rmtree(self.files_path, ignore_errors=True)
        os.makedirs(self.files_path, exist_ok=True)

    def get_sources(self):
        """
        Clone repository to sources folder
        """
        self.rm_sources()

        return git.Repo.clone_from(self.repository,  self.sources_path, branch='master')

    def rm_sources(self):
        """
        Remove sources
        """
        shutil.rmtree(self.sources_path, ignore_errors=True)
        return self

    def make_files(self):
        """
        Make files from sources
        """

        for source in config.SOURCE_DIRS:

            for root, dirs, files in os.walk(os.path.join(self.sources_path, source)):
                path = root.replace(self.sources_path, '')

                for file in files:
                    if not file.endswith(tuple(config.SOURCE_EXTENSIONS)):
                        continue
                    name = path + os.sep + file
                    with open(os.path.join(root + os.sep + file)) as source_file:
                        text = re.sub('@author.*', '', source_file.read())

                        # txt file generation
                        with open(self.txt_path, 'a+') as txt:
                            txt.write(
                                '{separator}\n{header}\n{separator}\n\n{text}\n\n'.format(
                                    separator='-' * 80, header=name, text=text
                                )
                            )
                        # html file generation
                        with open(self.html_path, 'a+') as html_file:
                            html_file.write(
                                '<h4>{header}</h4><pre>{text}</pre>'.format(
                                    separator='-' * 80, header=name, text=html.escape(text)
                                )
                            )

        return self

    def process(self):
        """
        Clone repository & make files
        """
        if self.sources_pull or not os.path.isdir(self.sources_path):
            self.get_sources()
        self.make_files()

        return self

    def __str__(self):
        """
        :return: str
        :rtype: str
        """
        return 'Mbs class: repository: {}, destination: {}'.format(self.repository, self.destination)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates sources files from git repository.')
    parser.add_argument('-r', '--repository', dest='repository', action='store', type=str, default=config.REPOSITORY_URL,
                        help='repository url (default: {})'.format(config.REPOSITORY_URL))

    parser.add_argument('-d', '--destination', dest='destination', action='store', type=str, default=config.DESTINATION,
                        help='destination folder (default: {})'.format(config.DESTINATION))

    parser.add_argument('-i', '--ignore_git_pull', dest='ignore_git_pull', action='store_true', default=False,
                        help='Do not pull sources')

    args = parser.parse_args()
    mbs = Mbs(destination=args.destination, repository=args.repository, sources_pull=not args.ignore_git_pull)
    mbs.process()

    print('{}Generation completed. Files directory: {}{}'.format('\033[92m', mbs.files_path, '\033[0m'))

