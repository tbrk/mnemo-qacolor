##############################################################################
#
# qacolor.py (by Timothy Bourke <tim@tbrk.org>)
#
# derived from custom_tag.py (by Peter Bienstman <Peter.Bienstman@UGent.be>)
# see also whiteonblack.py   (by Daniel Snider)
#
# Adds a custom tag <color> with optional attributes fg and bg taking
# X11 color names as values (see: http://en.wikipedia.org/wiki/X11_color_names)
#
# e.g. <color fg="red" bg="blue">
#
##############################################################################

from mnemosyne.core import *
from mnemosyne.pyqt_ui.plugin import get_main_widget
from qt import *
import re

##############################################################################
#
# Plugin to change the question and answer box colors.
#
##############################################################################

class QAColor(Plugin):
    version = "1.0.0"
    name = "QAColor"
    re_tag = re.compile(r'<color(\s+(fg\s*=\s*"(?P<fg>[^"]*)"|bg\s*=\s*"(?P<bg>[^"]*)"))*\s*/?>')

    def warn(self, msg):
        status = QMessageBox.information(None,
           self.main_dlg.trUtf8("Mnemosyne").append(": ").append(
                                self.name).append(" plugin"),
           msg,
           self.main_dlg.trUtf8("&OK"))

    def description(self):
        return ("Change question and answer box colors . (v" + version + ")")

    def load(self):
        self.main_dlg = get_main_widget()
        self.qbox = self.main_dlg.question
        self.abox = self.main_dlg.answer
        self.color = {}

        #self.orig_qbox_fgcolor = self.qbox.paletteForegroundColor()
        #self.orig_qbox_bgcolor = self.qbox.paletteBackgroundColor()
        #self.orig_abox_fgcolor = self.abox.paletteForegroundColor()
        #self.orig_abox_bgcolor = self.abox.paletteBackgroundColor()
        self.orig_qbox_fgcolor = self.get_color("black")
        self.orig_qbox_bgcolor = self.get_color("white")
        self.orig_abox_fgcolor = self.get_color("black")
        self.orig_abox_bgcolor = self.get_color("white")

        register_function_hook("filter_q", self.set_qbox_color)
        register_function_hook("filter_a", self.set_abox_color)

    def unload(self):
        self.set_box_colors(self.qbox, self.orig_qbox_fgcolor,
                                       self.orig_qbox_bgcolor)
        self.set_box_colors(self.abox, self.orig_abox_fgcolor,
                                       self.orig_abox_bgcolor)

        unregister_function_hook("filter_q", self.set_qbox_color)
        unregister_function_hook("filter_a", self.set_abox_color)
    
    def set_box_colors(self, box, fg, bg):
        box.setPaletteForegroundColor(fg)
        box.setPaletteBackgroundColor(bg)
    
    def get_color(self, name):
        if not self.color.has_key(name):
            self.color[name] = QColor(name)
        return self.color[name]
    
    def get_tag_colors(self, text, defaultfg, defaultbg):
        m = self.re_tag.search(text)

        if m == None:
            return (defaultfg, defaultbg)
        
        (fg, bg) = m.group("fg", "bg")
        if fg == None:
            fgc = defaultfg
        else:
            fgc = self.get_color(fg)

        if bg == None:
            bgc = defaultbg
        else:
            bgc = self.get_color(bg)

        return (fgc, bgc)
    
    def set_qbox_color(self, text, card):
        (fg, bg) = self.get_tag_colors(text, self.orig_qbox_fgcolor,
                                             self.orig_qbox_bgcolor)
        self.set_box_colors(self.qbox, fg, bg)
        self.set_box_colors(self.abox, self.orig_abox_fgcolor,
                                       self.orig_abox_bgcolor)
        return text

    def set_abox_color(self, text, card):
        (fg, bg) = self.get_tag_colors(text, self.orig_abox_fgcolor,
                                             self.orig_abox_bgcolor)
        self.set_box_colors(self.abox, fg, bg)
        return text

p = QAColor()
p.load()

