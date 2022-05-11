# Fork created from https://github.com/gajewsk2/anki-plugin-phonetics
# Copyright: Micah Gajewski <micahbgaj@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from anki.hooks import addHook
from aqt.qt import *

from .phonetics import regeneratePhonetics

buttonText = "Bulk-add Phonetics"

def onRegenerate(browser):
    regeneratePhonetics(browser.selected_notes())

def setupMenu(browser):
    a = QAction(buttonText, browser)
    a.triggered.connect(lambda: onRegenerate(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

addHook("browser.setupMenus", setupMenu)
