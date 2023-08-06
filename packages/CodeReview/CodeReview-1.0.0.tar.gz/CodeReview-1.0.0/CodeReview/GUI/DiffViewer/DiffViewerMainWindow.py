####################################################################################################
#
# CodeReview - A Code Review GUI
# Copyright (C) 2015 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging
import os

import pygments.lexers as pygments_lexers

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

####################################################################################################

from .DiffWidget import DiffView
from .LexerCache import LexerCache
from CodeReview.Diff.RawTextDocument import RawTextDocument
from CodeReview.Diff.RawTextDocumentDiff import TwoWayFileDiffFactory
from CodeReview.Diff.SyntaxHighlighter import HighlightedText, highlight_text
from CodeReview.Diff.TextDocumentDiffModel import TextDocumentDiffModelFactory, highlight_document
from CodeReview.Diff.TextDocumentModel import TextDocumentModel
from CodeReview.GUI.Base.MainWindowBase import MainWindowBase
from CodeReview.GUI.Widgets.IconLoader import IconLoader
from CodeReview.GUI.Widgets.MessageBox import MessageBox

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class DiffViewerMainWindow(MainWindowBase):

    _logger = _module_logger.getChild('DiffViewerMainWindow')

    closed = pyqtSignal()

    ##############################################

    def __init__(self, parent=None, repository=None):

        # Note: parent is None when diff viewer is the main application
        # Fixme: subclass standard and/ git diff

        super().__init__(title='CodeReview Diff Viewer', parent=parent)

        self._repository = repository
        self._staged = False # Fixme: only git

        self._current_path = None

        self._init_ui()
        self._create_actions()
        self._create_toolbar()

        icon_loader = IconLoader()
        self.setWindowIcon(icon_loader['code-review@svg'])

        self._lexer_cache = LexerCache()

        if self.is_main_window:
            self._application.directory_changed.connect(self._on_file_system_changed)
            self._application.file_changed.connect(self._on_file_system_changed)

    ##############################################

    def _init_ui(self):

        self._central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._vertical_layout = QtWidgets.QVBoxLayout(self._central_widget)

        self._message_box = MessageBox(self)
        self._diff_view = DiffView()

        for widget in (self._message_box, self._diff_view):
            self._vertical_layout.addWidget(widget)

    ##############################################

    def _create_actions(self):

        icon_loader = IconLoader()

        self._previous_file_action = \
            QtWidgets.QAction(icon_loader['go-previous@svg'],
                              'Previous',
                              self,
                              toolTip='Previous file',
                              shortcut='Ctrl+P',
                              triggered=self._previous_file,
            )

        self._next_file_action = \
            QtWidgets.QAction(icon_loader['go-next@svg'],
                              'Next',
                              self,
                              toolTip='Next file',
                              shortcut='Ctrl+N',
                              triggered=self._next_file,
            )

        self._refresh_action = \
            QtWidgets.QAction(icon_loader['view-refresh@svg'],
                              'Refresh',
                              self,
                              toolTip='Refresh',
                              shortcut='Ctrl+R',
                              triggered=self._refresh,
            )

        self._line_number_action = \
            QtWidgets.QAction(icon_loader['line-number-mode@svg'],
                              'Line Number Mode',
                              self,
                              toolTip='Line Number Mode',
                              shortcut='Ctrl+N',
                              checkable=True,
                              triggered=self._set_document_models,
            )

        self._align_action = \
            QtWidgets.QAction(icon_loader['align-mode@svg'],
                              'Align Mode',
                              self,
                              toolTip='Align Mode',
                              shortcut='Ctrl+L',
                              checkable=True,
                              triggered=self._set_document_models,
            )

        self._complete_action = \
            QtWidgets.QAction(icon_loader['complete-mode@svg'],
                              'Complete Mode',
                              self,
                              toolTip='Complete Mode',
                              shortcut='Ctrl+A',
                              checkable=True,
                              triggered=self._set_document_models,
            )

        self._highlight_action = \
            QtWidgets.QAction(icon_loader['highlight@svg'],
                              'Highlight',
                              self,
                              toolTip='Highlight text',
                              shortcut='Ctrl+H',
                              checkable=True,
                              triggered=self._refresh,
            )

        # Fixme: only git
        if self._repository:
            self._stage_action = \
                                 QtWidgets.QAction('Stage',
                                                   self,
                                                   toolTip='Stage file',
                                                   shortcut='Ctrl+S',
                                                   checkable=True,
                                                   triggered=self._stage,
                                 )
        else:
            self._stage_action = None

    ##############################################

    def _create_toolbar(self):

        self._algorithm_combobox = QtWidgets.QComboBox(self)
        for algorithm in ('Patience',):
            self._algorithm_combobox.addItem(algorithm, algorithm)
        self._algorithm_combobox.currentIndexChanged.connect(self._refresh)

        self._lines_of_context_combobox = QtWidgets.QComboBox(self)
        for number_of_lines_of_context in (3, 6, 12):
            self._lines_of_context_combobox.addItem(str(number_of_lines_of_context),
                                                    number_of_lines_of_context)
        self._lines_of_context_combobox.currentIndexChanged.connect(self._refresh)

        self._font_size_combobox = QtWidgets.QComboBox(self)
        min_font_size, max_font_size = 4, 20
        application_font_size = QtWidgets.QApplication.font().pointSize()
        min_font_size = min(min_font_size, application_font_size)
        max_font_size = max(max_font_size, application_font_size)
        for font_size in range(min_font_size, max_font_size +1):
            self._font_size_combobox.addItem(str(font_size), font_size)
        self._font_size_combobox.setCurrentIndex(application_font_size - min_font_size)
        self._font_size_combobox.currentIndexChanged.connect(self._on_font_size_change)
        self._on_font_size_change(refresh=False)

        if self._repository:
            self._status_label = QtWidgets.QLabel('Status: ???')
        else:
            self._status_label = None

        items = [
            self._algorithm_combobox,
            QtWidgets.QLabel(' '), # Fixme
            QtWidgets.QLabel('Context:'),
            self._lines_of_context_combobox,
            QtWidgets.QLabel(' '), # Fixme
            QtWidgets.QLabel('Font Size:'),
            self._font_size_combobox,
            self._line_number_action,
            self._align_action,
            self._complete_action,
            self._highlight_action,
            self._refresh_action,
            self._stage_action,
            self._status_label,
        ]
        if self._application._main_window is not None:
            self._patch_index_label = QtWidgets.QLabel()
            self.update_patch_index()
            items.extend((
                self._previous_file_action,
                self._patch_index_label,
                self._next_file_action,
            ))

        self._tool_bar = self.addToolBar('Diff Viewer')
        for item in items:
            if item is not None: # for self._stage_action
                if isinstance(item, QtWidgets.QAction):
                    self._tool_bar.addAction(item)
                else:
                    self._tool_bar.addWidget(item)

    ##############################################

    def init_menu(self):

        super().init_menu()

    ##############################################

    @property
    def is_main_window(self):
        return self.parent() is None
        # return self._application.main_window is self

    @property
    def is_not_main_window(self):
        return self.parent() is not None
        # return self._application.main_window is self

    ##############################################

    def closeEvent(self, event):

        # Fixme: else the window is reopened ???
        if self.is_main_window:
            self._application.directory_changed.disconnect(self._on_file_system_changed)
            self._application.file_changed.disconnect(self._on_file_system_changed)
        else:
            self.closed.emit()

        super().closeEvent(event)

    ##############################################

    def show_message(self, message=None, timeout=0, warn=False):

        """ Hides the normal status indications and displays the given message for the specified
        number of milli-seconds (timeout). If timeout is 0 (default), the message remains displayed
        until the clearMessage() slot is called or until the showMessage() slot is called again to
        change the message.

        Note that showMessage() is called to show temporary explanations of tool tip texts, so
        passing a timeout of 0 is not sufficient to display a permanent message.
        """

        if warn:
            self._message_box.push_message(message)
        else:
            status_bar = self.statusBar()
            if message is None:
                status_bar.clearMessage()
            else:
                status_bar.showMessage(message, timeout)

    ################################################

    def open_files(self, file1, file2, show=False):

        # Fixme: Actually it only supports file diff

        paths = (file1, file2)
        texts = (None, None)
        metadatas = [dict(path=file1, document_type='file', last_modification_date=None),
                     dict(path=file2, document_type='file', last_modification_date=None)]
        self.diff_documents(paths, texts, metadatas, show=show)

    ##############################################

    def _absolute_path(self, path):

        return os.path.join(self._workdir, path)

    ##############################################

    def _read_file(self, path):

        with open(self._absolute_path(path)) as f:
            text = f.read()
        return text

    ##############################################

    def _is_directory(self, path):

        if path is None:
            return False
        else:
            return os.path.isdir(self._absolute_path(path))

    ##############################################

    def _get_lexer(self, path, text):

        if path is None:
            return None

        return self._lexer_cache.guess(path, text)

    ##############################################

    def diff_documents(self, paths, texts, metadatas=None, workdir='', show=False):

        self._paths = list(paths)
        self._texts = list(texts)
        self._metadatas = metadatas
        self._workdir = workdir

        file1, file2 = self._paths
        if self._is_directory(file1) or self._is_directory(file2):
            self._highlighted_documents = [TextDocumentModel(metadata) for metadata in self._metadatas]
        else:
            self.diff_text_documents(show)

        self._set_document_models()

        if self._repository:
            self._staged = self._repository.is_staged(file2)
            self._status_label.clear()
            if self._repository.is_modified(file2):
                self._status_label.setText('<font color="red">Modified !</font>')
            if self._staged:
                self._logger.info("File {} is staged".format(file2))
            self._stage_action.blockSignals(True)
            self._stage_action.setChecked(self._staged)
            self._stage_action.blockSignals(False)

        # Fixme:
        # Useless if application is LogBrowserApplication
        # file_system_watcher = self._application.file_system_watcher
        # files = file_system_watcher.files()
        # if files:
        #     file_system_watcher.removePaths(files)
        # self._logger.info("Monitor {}".format(file2))
        # file_system_watcher.addPath(file2)

    ##############################################

    def diff_text_documents(self, show=False):

        OLD, NEW = list(range(2))
        for i in (OLD, NEW):
            if self._paths[i] is None:
                self._texts[i] = ''
            elif self._texts[i] is None:
                self._texts[i] = self._read_file(self._paths[i])
        lexers = [self._get_lexer(path, text) for path, text in zip(self._paths, self._texts)]
        raw_text_documents = [RawTextDocument(text) for text in self._texts]

        highlight = self._highlight_action.isChecked()
        number_of_lines_of_context = self._lines_of_context_combobox.currentData()

        self._highlighted_documents = []
        if not show:
            file_diff = TwoWayFileDiffFactory().process(* raw_text_documents,
                                                        number_of_lines_of_context=number_of_lines_of_context)
            document_models = TextDocumentDiffModelFactory().process(file_diff)
            for raw_text_document, document_model, lexer in zip(raw_text_documents, document_models, lexers):
                if lexer is not None and highlight:
                    highlighted_text = HighlightedText(raw_text_document, lexer)
                    highlighted_document = highlight_document(document_model, highlighted_text)
                else:
                    highlighted_document = document_model
                self._highlighted_documents.append(highlighted_document)
        else: # Only show the document
            # Fixme: broken, chunk_type is ???
            # self._diff_view.set_document_models(self._highlighted_documents, complete_mode)
            # File "/home/gv/fabrice/unison-osiris/git-python/CodeReview/DiffWidget.py", line 333, in set_document_models
            # cursor.begin_block(side, text_block.frame_type)
            # File "/home/gv/fabrice/unison-osiris/git-python/CodeReview/DiffWidget.py", line 99, in begin_block
            # if ((side == LEFT and frame_type == chunk_type.insert) or
            # File "/home/gv/fabrice/unison-osiris/git-python/CodeReview/Tools/EnumFactory.py", line 107, in __eq__
            # return self._value == int(other)
            # TypeError: int() argument must be a string or a number, not 'NoneType'
            for raw_text_document, lexer in zip(raw_text_documents, self._lexers):
                highlighted_document = highlight_text(raw_text_document, lexer)
                self._highlighted_documents.append(highlighted_document)

        if self._metadatas is not None:
            for highlighted_document, metadata in zip(self._highlighted_documents, self._metadatas):
                highlighted_document.metadata = metadata

    ################################################

    def _set_document_models(self):

        aligned_mode = self._align_action.isChecked()
        complete_mode = self._complete_action.isChecked()
        line_number_mode = self._line_number_action.isChecked()
        # Fixme: right way ?
        self._diff_view.set_document_models(self._highlighted_documents,
                                            aligned_mode, complete_mode, line_number_mode)

    ##############################################

    def _on_font_size_change(self, index=None, refresh=True):

        self._diff_view.set_font(self._font_size_combobox.currentData())
        if refresh:
            self._refresh() # Fixme: block position are not updated

    ##############################################

    def _on_file_system_changed(self, path):

        # only used for main window

        self._logger.info(path)
        self._refresh()

    ##############################################

    def _refresh(self):

        if self.is_main_window:
            # Fixme: better way ???
            texts = (None, None) # to force to reread files
            self.diff_documents(self._paths, texts, self._metadatas, self._workdir) # Fixme: show ???
        else:
            main_window = self.parent()
            main_window.reload_current_patch()

    ##############################################

    def update_patch_index(self):

        main_window = self.parent()
        self._patch_index_label.setText('{}/{}'.format(
            main_window.current_patch_index +1,
            main_window.number_of_patches))

    ##############################################

    def _previous_next_file(self, forward):

        # Fixme: only for Git
        if self.is_not_main_window:
            main_window = self.parent()
            if forward:
                main_window.next_patch()
            else:
                main_window.previous_patch()
            self.update_patch_index()
        # else: directory diff is not implemented

    ##############################################

    def _previous_file(self):
        self._previous_next_file(False)

    ##############################################

    def _next_file(self):
        self._previous_next_file(True)

    ##############################################

    def _stage(self):

        # Fixme: only for Git

        file_path = self._paths[1]
        if self._staged:
            self._repository.unstage(file_path)
            action = 'Unstage'
        else:
            self._repository.stage(file_path)
            action = 'Stage'
        self._logger.info("{} {}".format(action, file_path))
        self._staged = not self._staged
