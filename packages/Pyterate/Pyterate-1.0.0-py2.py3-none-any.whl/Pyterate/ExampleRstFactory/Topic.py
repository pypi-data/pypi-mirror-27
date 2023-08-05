####################################################################################################
#
# Pyterate - Sphinx add-ons to create API documentation for Python projects
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

""" This module implements a RST files generator for examples.
"""

####################################################################################################

import glob
import logging
import os

from .Document import Document
from .Template import *

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

def sublist_accumulator_iterator(iterable):
    """ From a list (1, 2, 3, ...) this generator yields (), (1,), (1, 2), (1, 2, 3), ... """
    for i in range(len(iterable) +1):
        yield iterable[:i]

####################################################################################################

class Topic:

    _logger = _module_logger.getChild('Topic')

    ##############################################

    def __init__(self, factory, relative_path):

        self._factory = factory
        self._relative_path = relative_path
        self._basename = os.path.basename(relative_path)

        self._path = self._factory.join_examples_path(relative_path)
        self._rst_path = self._factory.join_rst_example_path(relative_path)

        self._subtopics = [] # self._retrieve_subtopics()
        self._examples = []
        self._links = []
        python_files = [filename for filename in self._python_files_iterator()
                        if self._filter_python_files(self._path, filename)]
        if python_files:
            self._logger.info("\nProcess Topic: " + relative_path)
            self._make_hierarchy()
            for filename in python_files:
                example = Document(self, filename)
                if example.is_link:
                    self._logger.info("\n  found link: " + filename)
                    self._links.append(example)
                else:
                    self._logger.info("\n  found: " + filename)
                    self._examples.append(example)

    ##############################################

    def __bool__(self):
        return os.path.exists(self._rst_path)
        # return bool(self._examples) or bool(self._links)

    ##############################################

    @property
    def factory(self):
        return self._factory

    @property
    def basename(self):
        return self._basename

    @property
    def path(self):
        return self._path

    @property
    def rst_path(self):
        return self._rst_path

    ##############################################

    def join_path(self, filename):
        return os.path.join(self._path, filename)

    def join_rst_path(self, filename):
        return os.path.join(self._rst_path, filename)

    ##############################################

    def _files_iterator(self, extension):

        pattern = os.path.join(self._path, '*.' + extension)
        for file_path in glob.glob(pattern):
            yield os.path.basename(file_path)

    ##############################################

    def _python_files_iterator(self):

        return self._files_iterator('py')

    ##############################################

    @staticmethod
    def _filter_python_files(path, filename):

        if filename.endswith('.py'):
            # these file should be flymake temporary file
            for pattern in ('flymake_', 'flycheck_'):
                if filename.startswith(pattern):
                    return False
            absolut_path = os.path.join(path, filename)
            with open(absolut_path, 'r') as fh:
                first_line = fh.readline()
                second_line = fh.readline()
                pattern = '#skip#'
                return not (first_line.startswith(pattern) or second_line.startswith(pattern))

        return False

    ##############################################

    def _readme_path(self):
        return self.join_path('readme.rst')

    ##############################################

    def _has_readme(self):
        return os.path.exists(self._readme_path())

    ##############################################

    def _read_readme(self, make_external_figure):

        figures = [] # Fixme: unused, purpose (*) ???
        image_directive = '.. image:: '
        image_directive_length = len(image_directive)
        with open(self._readme_path()) as fh:
            content = fh.read()
            for line in content.split('\n'):
                if line.startswith(image_directive):
                    figure = line[image_directive_length:]
                    figures.append(figure)

        # Fixme: (*) tikz ???
        # if make_external_figure:
        # ...

        return content

    ##############################################

    def _example_hierarchy(self):

        """ Return a list of directory corresponding to the file hierarchy after ``.../examples/`` """

        return self._relative_path.split(os.path.sep)

    ##############################################

    def _make_hierarchy(self):

        """ Create the file hierarchy. """

        example_hierarchy = self._example_hierarchy()
        for directory_list in sublist_accumulator_iterator(example_hierarchy):
            directory = self._factory.join_rst_example_path(*directory_list)
            if not os.path.exists(directory):
                os.mkdir(directory)

    ##############################################

    def process_examples(self, make_figure, make_external_figure, force):

        for example in self._examples:
            self.process_example(example, make_figure, make_external_figure, force)

    ##############################################

    def process_example(self, example, make_figure, make_external_figure, force):

        example.read()
        if force or example:
            if make_figure:
                example.make_figure()
            example.make_rst()
        if make_external_figure:
            example.make_external_figure(force)

    ##############################################

    def _retrieve_subtopics(self):

        if not self:
            return None

        subtopics = []
        for filename in os.listdir(self._rst_path):
            path = self.join_rst_path(filename)
            if os.path.isdir(path):
                if os.path.exists(os.path.join(path, 'index.rst')):
                    relative_path = os.path.relpath(path, self._factory.rst_example_directory)
                    topic = self._factory.topics[relative_path]
                    subtopics.append(topic)
        self._subtopics = subtopics

    ##############################################

    def make_toc(self, make_external_figure):

        """ Create the TOC. """

        if not self: # Fixme: when ???
            return

        toc_path = self.join_rst_path('index.rst')
        self._logger.info("\nCreate TOC " + toc_path)

        content = ''

        if self._has_readme():
            content += self._read_readme(make_external_figure)
        else:
            title = self._basename.replace('-', ' ').title() # Fixme: Capitalize of
            title_line = '='*(len(title)+2)
            if title:
                content += TITLE_TEMPLATE.format(title=title, title_line=title_line)

        # Sort the TOC
        # Fixme: sometimes we want a particular order !
        file_dict = {example.basename:example.rst_filename for example in self._examples}
        file_dict.update({link.basename:link.rst_inner_path for link in self._links})
        toc_items = sorted(file_dict.keys())

        self._retrieve_subtopics()
        subtopics = [topic.basename for topic in self._subtopics]

        if self._factory.show_counter:
            self._number_of_examples = len(self._examples) # don't count links twice
            number_of_links = len(self._links)
            number_of_subtopics = sum([topic._number_of_examples for topic in self._subtopics])
            number_of_examples = self._number_of_examples + number_of_subtopics
            counter_strings = []
            if self._subtopics:
                counter_strings.append('{} sub-topics'.format(len(self._subtopics)))
            if number_of_examples:
                counter_strings.append('{} examples'.format(number_of_examples))
            if number_of_links:
                counter_strings.append('{} related examples'.format(number_of_links))
            if counter_strings:
                content += 'This section has '
                if len(counter_strings) == 1:
                    content += counter_strings[0]
                elif len(counter_strings) == 2:
                    content += counter_strings[0] + ' and ' + counter_strings[1]
                elif len(counter_strings) == 3:
                    content += counter_strings[0] + ', ' + counter_strings[1] + ' and ' + counter_strings[2]
                content += '.\n'

        with open(toc_path, 'w') as fh:
            fh.write(content)
            fh.write(TOC_TEMPLATE)
            for subtopic in sorted(subtopics):
                fh.write('  {}/index.rst\n'.format(subtopic))
            for key in toc_items:
                filename = file_dict[key]
                fh.write('  {}\n'.format(filename))
