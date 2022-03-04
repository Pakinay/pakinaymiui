# Copyright (C) 2011 Chris Dekter
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

from gi.repository import Gtk, Gdk


class GtkClipboard:
    """
    Read/write access to the X selection and clipboard - GTK version
    """

    def __init__(self, app):
        self.clipBoard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.selection = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.app = app

    def fill_selection(self, contents):
        """
        Copy text into the X selection

        Usage: C{clipboard.fill_selection(contents)}

        @param contents: string to be placed in the selection
        """
        #self.__execAsync(self.__fillSelection, contents)
        self.__fillSelection(contents)

    def __fillSelection(self, string):
        Gdk.threads_enter()
        self.selection.set_text(string, -1)
        Gdk.threads_leave()
        #self.sem.release()

    def get_selection(self):
        """
        Read text from the X selection

        Usage: C{clipboard.get_selection()}

        @return: text contents of the mouse selection
        @rtype: C{str}
        @raise Exception: if no text was found in the selection
        """
        Gdk.threads_enter()
        text = self.selection.wait_for_text()
        Gdk.threads_leave()
        if text is not None:
            return text
        else:
            raise Exception("No text found in X selection")

    def fill_clipboard(self, contents):
        """
        Copy text into the clipboard

        Usage: C{clipboard.fill_clipboard(contents)}

        @param contents: string to be placed in the selection
        """
        Gdk.threads_enter()
        if Gtk.get_major_version() >= 3:
            self.clipBoard.set_text(contents, -1)
        else:
            self.clipBoard.set_text(contents)
        Gdk.threads_leave()

    def get_clipboard(self):
        """
        Read text from the clipboard

        Usage: C{clipboard.get_clipboard()}

        @return: text contents of the clipboard
        @rtype: C{str}
        @raise Exception: if no text was found on the clipboard
        """
        Gdk.threads_enter()
        text = self.clipBoard.wait_for_text()
        Gdk.threads_leave()
        if text is not None:
            return text
        else:
            raise Exception("No text found on clipboard")
