from aqt import mw
from . import parser

config = mw.addonManager.getConfig(__name__)

srcFields = config["srcFields"]
dstFields = config["dstFields"]

def regeneratePhonetics(nids):
    mw.checkpoint("JapanesePhoneticComponents")
    mw.progress.start()

    for nid in nids:
        note = mw.col.get_note(nid)

        fields_length = min(len(srcFields), len(dstFields))

        for (src, dst) in zip(srcFields[:fields_length], dstFields[:fields_length]):
            if src not in note or dst not in note:
                continue

            if note[dst]:
                # already contains data, skip
                continue

            srcTxt = mw.col.media.strip(note[src]).strip()
            if not srcTxt:
                # no source data
                continue

            try:
                note[dst] = parser.getHighlightedPhonetics(srcTxt)
            except Exception as e:
                raise e

        note.flush()

    mw.progress.finish()
    mw.reset()
