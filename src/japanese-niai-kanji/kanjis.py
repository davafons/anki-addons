from aqt import mw
from . import parser


def regenerateSimilarKanjis(nids):
    config = mw.addonManager.getConfig(__name__)

    srcFields = config["srcFields"]
    dstFields = config["dstFields"]

    mw.checkpoint("JapaneseSimilarKanjis")
    mw.progress.start()

    for nid in nids:
        note = mw.col.get_note(nid)

        fields_length = min(len(srcFields), len(dstFields))

        for (src, dst) in zip(srcFields[:fields_length], dstFields[:fields_length]):
            if src not in note or dst not in note:
                # missing fields, skip
                continue

            if note[dst]:
                # already contains data, skip
                continue

            srcTxt = mw.col.media.strip(note[src]).strip()
            if not srcTxt:
                # no source data
                continue

            try:
                note[dst] = parser.getSimilarKanjis(srcTxt)
            except Exception as e:
                raise e

        note.flush()

    mw.progress.finish()
    mw.reset()
