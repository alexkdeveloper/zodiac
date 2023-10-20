# window.py
#
# Copyright 2023 Alex
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
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from datetime import datetime
from pathlib import Path
from kerykeion import AstrologicalSubject, KerykeionChartSVG, Report

@Gtk.Template(resource_path='/io/github/alexkdeveloper/zodiac/window.ui')
class ZodiacWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ZodiacWindow'

    drop_down = Gtk.Template.Child()
    show_button = Gtk.Template.Child()
    open_button = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()
    save_button = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    svg = Gtk.Template.Child()
    text = Gtk.Template.Child()
    overlay = Gtk.Template.Child()
    result_page = Gtk.Template.Child()
    data_page = Gtk.Template.Child()
    entry_name = Gtk.Template.Child()
    entry_day = Gtk.Template.Child()
    entry_year = Gtk.Template.Child()
    entry_hours = Gtk.Template.Child()
    entry_minutes = Gtk.Template.Child()
    entry_place = Gtk.Template.Child()
    entry_save = Gtk.Template.Child()
    combo = Gtk.Template.Child()
    data_page2 = Gtk.Template.Child()
    entry_name2 = Gtk.Template.Child()
    entry_day2 = Gtk.Template.Child()
    entry_year2 = Gtk.Template.Child()
    entry_hours2 = Gtk.Template.Child()
    entry_minutes2 = Gtk.Template.Child()
    entry_place2 = Gtk.Template.Child()
    combo2 = Gtk.Template.Child()

    path = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.show_button.connect("clicked", self.on_show_clicked)
        self.open_button.connect("clicked", self.on_open_clicked)
        self.back_button.connect("clicked", self.on_back_clicked)
        self.next_button.connect("clicked", self.on_next_clicked)
        self.save_button.connect("clicked", self.show_open_dialog)
        self.drop_down.connect("notify::selected-item", self.item_selected)

        self.back_button.set_visible(False)
        self.next_button.set_visible(False)
        self.open_button.set_visible(False)

        settings = Gio.Settings(schema_id="io.github.alexkdeveloper.zodiac")

        settings.bind("width", self, "default-width", Gio.SettingsBindFlags.DEFAULT)
        settings.bind("height", self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        settings.bind("is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT)
        settings.bind("is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT)

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title(_("Select a Folder"))

    def show_open_dialog(self, widget):
        self.open_dialog.select_folder(self, None, self.open_dialog_open_callback)

    def open_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.select_folder_finish(result)
            if file is not None:
                self.entry_save.set_text(file.get_path())
        except GLib.Error as error:
            print(f"Error select folder: {error.message}")

    def item_selected(self, widget, _):
        if self.drop_down.get_selected() == 0:
           self.show_button.set_visible(True)
           self.next_button.set_visible(False)
        else:
           self.show_button.set_visible(False)
           self.next_button.set_visible(True)

    def on_show_clicked(self, widget):
        if len(self.entry_name.get_text().strip()) == 0 or len(self.entry_day.get_text().strip()) == 0 or len(self.entry_year.get_text().strip()) == 0 or len(self.entry_hours.get_text().strip()) == 0 or len(self.entry_minutes.get_text().strip()) == 0 or len(self.entry_place.get_text().strip()) == 0 or len(self.entry_save.get_text().strip()) == 0:
           self.set_toast(_("Fill in all the fields!"))
           return

        name = self.entry_name.get_text()
        day = int(self.entry_day.get_text())
        month = self.combo.get_selected()+1
        year = int(self.entry_year.get_text())
        hours = int(self.entry_hours.get_text())
        minutes = int(self.entry_minutes.get_text())
        place = self.entry_place.get_text()

        if not self.is_valid_date_time(day, month, year, hours, minutes):
           self.set_toast(_("Enter valid date and time of birth values"))
           return

        report_text = ""

        if self.drop_down.get_selected() == 0:
           subject = AstrologicalSubject(name, year, month, day, hours, minutes, place)
           chart = KerykeionChartSVG(subject, chart_type="Natal")

           report = Report(subject)

           report_text = report.get_full_report()

           subject_names = name
        else:
           if len(self.entry_name2.get_text().strip()) == 0 or len(self.entry_day2.get_text().strip()) == 0 or len(self.entry_year2.get_text().strip()) == 0 or len(self.entry_hours2.get_text().strip()) == 0 or len(self.entry_minutes2.get_text().strip()) == 0 or len(self.entry_place2.get_text().strip()) == 0:
              self.set_toast(_("Fill in all the fields!"))
              return

           name2 = self.entry_name2.get_text()
           day2 = int(self.entry_day2.get_text())
           month2 = self.combo2.get_selected()+1
           year2 = int(self.entry_year2.get_text())
           hours2 = int(self.entry_hours2.get_text())
           minutes2 = int(self.entry_minutes2.get_text())
           place2 = self.entry_place2.get_text()

           if not self.is_valid_date_time(day2, month2, year2, hours2, minutes2):
              self.set_toast(_("Enter valid date and time of birth values"))
              return

           subject = AstrologicalSubject(name, year, month, day, hours, minutes, place)
           subject2 = AstrologicalSubject(name2, year2, month2, day2, hours2, minutes2, place2)

           chart = KerykeionChartSVG(subject, chart_type="Synastry", second_obj=subject2)

           report = Report(subject)
           report2 = Report(subject2)

           report_text = report.get_full_report()+"\n"+report2.get_full_report()

           subject_names = name+name2

        self.path = self.entry_save.get_text()

        path_to_report = self.path+"/"+subject_names+"Report.txt"

        with open(path_to_report, 'w') as f:
             f.write(report_text)

        chart.set_output_directory(Path(self.path))
        chart.makeSVG()

        path_to_chart = self.path+"/"+name+chart.chart_type+"Chart.svg"

        self.svg.set_from_file(path_to_chart)

        self.text.set_text(report_text)

        if Path(path_to_chart).exists() and Path(path_to_report).exists():
            self.set_toast(_("Files saved successfully"))
        elif not Path(path_to_chart).exists() and Path(path_to_report).exists():
            self.set_toast(_("Failed to save svg file"))
        elif Path(path_to_chart).exists() and not Path(path_to_report).exists():
            self.set_toast(_("Failed to save txt file"))
        else:
            self.set_toast(_("Failed to save files"))

        self.stack.set_visible_child(self.result_page)
        self.back_button.set_visible(True)
        self.drop_down.set_visible(False)
        self.next_button.set_visible(False)
        self.show_button.set_visible(False)
        self.open_button.set_visible(True)

    def is_valid_date_time(self, day, month, year, hours, minutes):
        try:
           datetime(year, month, day, hours, minutes)
           return True
        except ValueError:
           return False

    def on_back_clicked(self, widget):
        if self.drop_down.get_selected() == 0:
           self.stack.set_visible_child(self.data_page)
           self.back_button.set_visible(False)
           self.next_button.set_visible(False)
           self.drop_down.set_visible(True)
           self.show_button.set_visible(True)
           self.open_button.set_visible(False)
        else:
           if self.stack.get_visible_child() == self.result_page:
              self.stack.set_visible_child(self.data_page2)
              self.back_button.set_visible(True)
              self.next_button.set_visible(False)
              self.drop_down.set_visible(False)
              self.show_button.set_visible(True)
              self.open_button.set_visible(False)
           else:
              self.stack.set_visible_child(self.data_page)
              self.back_button.set_visible(False)
              self.next_button.set_visible(True)
              self.drop_down.set_visible(True)
              self.show_button.set_visible(False)
              self.open_button.set_visible(False)

    def on_next_clicked(self, widget):
        self.stack.set_visible_child(self.data_page2)
        self.back_button.set_visible(True)
        self.next_button.set_visible(False)
        self.drop_down.set_visible(False)
        self.show_button.set_visible(True)
        self.open_button.set_visible(False)

    def on_open_clicked(self, widget):
        Gtk.show_uri(None, "file://"+self.path, Gdk.CURRENT_TIME)

    def set_toast(self, str):
        toast = Adw.Toast.new(str)
        toast.set_timeout(4)
        self.overlay.add_toast(toast)
