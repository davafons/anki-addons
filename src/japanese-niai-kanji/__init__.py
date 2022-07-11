from anki.hooks import addHook
from aqt.qt import *

from .kanjis import regenerateSimilarKanjis

buttonText = "Bulk-add Similar Kanjis"


def onRegenerate(browser):
    regenerateSimilarKanjis(browser.selected_notes())


def setupMenu(browser):
    a = QAction(buttonText, browser)
    a.triggered.connect(lambda: onRegenerate(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)


addHook("browser.setupMenus", setupMenu)
