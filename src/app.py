import sys
import os
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk

import utils


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_name("dictionary")

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.set_show_title_buttons(True)
        titleWidget = Gtk.Label.new("Dictionary")
        self.headerBar.props.title_widget = titleWidget
        self.set_titlebar(self.headerBar)

        self.headerGoHome = Gtk.Button(label="")
        self.headerGoHome.set_icon_name("go-home")
        self.headerGoHome.connect("clicked", self.show_history)
        self.headerBar.pack_start(self.headerGoHome)
        aboutAction = Gio.SimpleAction.new("showabout", None)
        aboutAction.connect("activate", self.show_about)
        self.add_action(aboutAction)
        # showSetLang=Gio.SimpleAction.new("showSetLang", None)
        # showSetLang.connect("activate", self.show_about)
        # self.add_action(showSetLang)
        menu = Gio.Menu.new()
        # menu.append("Set Language", "win.showSetLang")
        menu.append("About", "win.showabout")
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)
        self.hamburger = Gtk.MenuButton()
        self.hamburger.set_popover(self.popover)
        self.hamburger.set_icon_name("open-menu-symbolic")
        self.headerBar.pack_start(self.hamburger)

        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.mainBox)
        self.mainBox.set_spacing(20)
        self.mainBox.set_margin_start(20)
        self.mainBox.set_margin_end(20)
        self.mainBox.set_margin_top(20)
        self.mainBox.set_margin_bottom(20)

        self.mainSearchEntry = Gtk.Entry()
        self.mainSearchEntry.set_placeholder_text("What do you want to search for?")
        self.mainSearchEntry.props.xalign = 0.5  # Center text
        self.mainBox.append(self.mainSearchEntry)

        self.mainSearchButton = Gtk.Button(label="Search")
        self.mainBox.append(self.mainSearchButton)
        self.mainSearchButton.connect("clicked", self.find_word)

        self.foundBox = None
        self.historyBox = None

        self.show_history()

    def show_history(self, action=None, pref=None):
        if self.foundBox != None:
            self.mainBox.remove(self.foundBox)
            self.foundBox = None
        if self.historyBox != None:
            self.mainBox.remove(self.historyBox)
            self.historybox = None
        self.historyBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.historyBox.set_spacing(20)
        self.mainBox.append(self.historyBox)
        subHistoryBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        subHistoryBox.set_spacing(20)
        previousSearchText = Gtk.Label()
        previousSearchText.set_markup(
            '<span size="10500"><b>Recently Searched</b></span>'
        )
        self.historyBox.append(previousSearchText)
        subHistoryBox = Gtk.FlowBox(orientation=Gtk.Orientation.HORIZONTAL)
        subHistoryBox.set_row_spacing(20)
        subHistoryBox.set_column_spacing(20)
        if len(utils.currentHist) == 0:
            historyEmptyLabel = Gtk.Label()
            historyEmptyLabel.set_markup('<span size="10000">Nothing in history</span>')
            self.historyBox.append(historyEmptyLabel)
            return
        for item in utils.currentHist:
            hist_btn = Gtk.Button(label="")
            hist_btn.get_child().set_markup(f'<span size="9000">{item}</span>')
            hist_btn.connect("clicked", self.find_word, item)
            subHistoryBox.append(hist_btn)
        self.historyBox.append(subHistoryBox)
        clearHistBtn = Gtk.Button(label="")
        clearHistBtn.get_child().set_markup(f'<span size="9500">Clear History</span>')
        clearHistBtn.connect("clicked", self.clearHistory)
        self.historyBox.append(clearHistBtn)

    def clearHistory(self, action=None, pref=None):
        utils.clear_history("en")  # Handle language by user preference
        self.show_history()

    def show_about(self, action, pref):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(
            self
        )  # Makes the dialog always appear in from of the parent window
        self.about.set_modal(
            self
        )  # Makes the parent window unresponsive while dialog is showing

        self.about.set_authors(["Nannan"])
        self.about.set_program_name("Dictionary")
        self.about.set_license_type(Gtk.License.MPL_2_0)
        self.about.set_website("http://www.github.com/nanna7077/Dictionary")
        self.about.set_website_label("GitHub")
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("Dictionary")
        self.about.show()

    def find_word(self, action=None, passedSearchTerm_=None):
        passedSearchTerm = passedSearchTerm_
        if self.historyBox != None:
            self.mainBox.remove(self.historyBox)
            self.historyBox = None
        # Use language specific handler from user preference
        if passedSearchTerm != None:
            searchTerm = passedSearchTerm
            word, wordData, directFind = utils.en_search(passedSearchTerm)
        else:
            searchTerm = self.mainSearchEntry.get_text()
            if searchTerm == None or len(searchTerm.strip()) == 0:
                self.mainSearchEntry.grab_focus()
                return
            word, wordData, directFind = utils.en_search(
                searchTerm
            )  # Use language specific search and handler's from user preference.
        if self.foundBox != None:
            self.mainBox.remove(self.foundBox)
            self.foundBox = None
        self.foundBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.foundBox.set_spacing(20)
        self.mainBox.append(self.foundBox)
        if not directFind:
            notDirectFind = Gtk.Label()
            notDirectFind.set_markup(
                f'<span size="10000">Could not find <i>{searchTerm}</i>, did you mean <b>{word}</b>?</span>'
            )
            self.foundBox.append(notDirectFind)
        self.wordDisp = Gtk.Label()
        self.wordDisp.set_markup(f'<span size="20000">{word}</span>')
        self.foundBox.append(self.wordDisp)
        c = 1
        for i in wordData["MEANINGS"]:
            meaningDisp = Gtk.Label()
            meaningDisp.set_markup(
                f"<span size=\"10000\">{c}. <b>{wordData['MEANINGS'][i][0]}</b>\n{wordData['MEANINGS'][i][1]}\nExample, {'; '.join(wordData['MEANINGS'][i][3])}</span>"
            )
            self.foundBox.append(meaningDisp)
            c += 1
        utils.save_history(
            "en", searchTerm
        )  # Change to dynamic based on user preferred language

    def on_activate(self, app):
        if not self.win:
            self.win = MainWindow(application=app)
        self.win.present()


class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


app = App(application_id="com.ghosty.Dictionary")
app.run(sys.argv)
