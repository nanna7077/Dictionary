import sys
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, Gdk

import utils

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon_name('dictionary') # Should load icon from the system since Dictionary is a pretty common icon.

        self.headerBar=Gtk.HeaderBar()
        self.headerBar.set_show_title_buttons(True)
        titleWidget=Gtk.Label.new("Dictionary")
        self.headerBar.props.title_widget=titleWidget
        self.set_titlebar(self.headerBar)

        aboutAction=Gio.SimpleAction.new("showabout", None)
        aboutAction.connect("activate", self.show_about)
        self.add_action(aboutAction)
        # showSetLang=Gio.SimpleAction.new("showSetLang", None)
        # showSetLang.connect("activate", self.show_about)
        # self.add_action(showSetLang)
        menu = Gio.Menu.new()
        # menu.append("Set Language", "win.showSetLang")
        menu.append("About", "win.showabout")
        self.popover=Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)
        self.hamburger=Gtk.MenuButton()
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

        self.mainSearchEntry=Gtk.Entry()
        self.mainSearchEntry.set_placeholder_text("What do you want to search for?")
        self.mainSearchEntry.props.xalign=0.5 # Center text
        self.mainBox.append(self.mainSearchEntry)

        self.mainSearchButton=Gtk.Button(label="Search")
        self.mainBox.append(self.mainSearchButton)
        self.mainSearchButton.connect('clicked', self.find_word)        

        self.foundBox=None
    
    def show_about(self, action, pref):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)  # Makes the dialog always appear in from of the parent window
        self.about.set_modal(self)  # Makes the parent window unresponsive while dialog is showing

        self.about.set_authors(["Nannan"])
        self.about.set_program_name("Dictionary")
        self.about.set_license_type(Gtk.License.MPL_2_0)
        self.about.set_website("http://www.github.com/nanna7077") # Change to repo link later
        self.about.set_website_label("GitHub")
        self.about.set_version("1.0")
        self.about.set_logo_icon_name("org.ghosty.Dictionary")  # The icon will need to be added to appropriate location
                                                 # E.g. /usr/share/icons/hicolor/scalable/apps/org.example.example.svg
        self.about.show()
    
    def find_word(self, action):
        searchTerm=self.mainSearchEntry.get_text()
        if searchTerm==None or len(searchTerm.strip())==0:
            self.mainSearchEntry.grab_focus()
            return
        # Use language specific handler from user preference
        word, wordData, directFind=utils.en_search(searchTerm) # Use language specific search and handler's from user preference.
        if self.foundBox!=None:
            self.mainBox.remove(self.foundBox)
            self.foundBox=None
        self.foundBox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.foundBox.set_spacing(20)
        self.mainBox.append(self.foundBox)
        if not directFind:
            notDirectFind=Gtk.Label()
            notDirectFind.set_markup(f"<span size=\"10000\">Could not find <i>{searchTerm}</i>, did you mean <b>{word}</b>?</span>")
            self.foundBox.append(notDirectFind)
        self.wordDisp=Gtk.Label()
        self.wordDisp.set_markup(f"<span size=\"20000\">{word}</span>")
        self.foundBox.append(self.wordDisp)
        c=1
        for i in wordData['MEANINGS']:
            meaningDisp=Gtk.Label()
            meaningDisp.set_markup(f"<span size=\"10000\">{c}. <b>{wordData['MEANINGS'][i][0]}</b>\n{wordData['MEANINGS'][i][1]}\nExample, {'; '.join(wordData['MEANINGS'][i][3])}</span>")
            self.foundBox.append(meaningDisp)
            c+=1

    def on_activate(self, app):
        if not self.win:
            self.win=MainWindow(application=app)
        self.win.present()

class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = App(application_id="com.ghosty.Dictionary")
app.run(sys.argv)