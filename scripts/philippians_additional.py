#!/usr/bin/env python3
"""Add ADDITIONAL TRANSLATION NOTES to Philippians chapters."""
import os

base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/11 - Philippians"

notes = dict()

notes[1] = """v.6  — NET: "I am sure of this very thing, that the one who
       began a good work in you will perfect it until the day of
       Christ Jesus" — "perfect" (epitelesei = complete/bring to
       fulfillment). WEB: "he who began a good work in you will
       complete it." KJV: "he which hath begun a good work in you
       will perform it." God finishes what He starts — perseverance
       is His responsibility.

v.21 — NET: "For to me, living is Christ and dying is gain" —
       "living IS Christ" (to zEn Christos) — not "living is FOR
       Christ" but Christ is the content of life itself. WEB: "to
       me to live is Christ, and to die is gain." KJV: "to live is
       Christ, and to die is gain." The most compressed life
       philosophy in Scripture.

v.23 — NET: "I am torn between the two" — "torn" (synechomai =
       pressed/hemmed in from both sides). WEB: "I am in a
       dilemma." KJV: "I am in a strait betwixt two." A genuine
       tension: depart to be with Christ (better for Paul) or
       remain (better for them).

v.27 — NET: "conduct yourselves in a manner worthy of the gospel
       of Christ" — "conduct yourselves" (politeuesthe = live as
       citizens). WEB: "let your way of life be worthy." The word
       is political — live as citizens of heaven (3:20) while
       resident on earth.

v.29 — NET: "For it has been granted to you not only to believe
       in Christ but also to suffer for his sake" — "granted"
       (echaristhE = graced/gifted). WEB: "it has been granted to
       you on behalf of Christ... to suffer." Suffering is a
       gift (charisma) — not just an accident."""

notes[2] = """v.5  — NET: "You should have the same attitude toward one
       another that Christ Jesus had" — "attitude" (phronein =
       mindset/way of thinking). WEB: "Have this in your mind,
       which was also in Christ Jesus." KJV: "Let this mind be in
       you, which was also in Christ Jesus." The Christ Hymn
       (vv.6-11) follows as the model.

v.6  — NET: "who though he existed in the form of God did not
       regard equality with God as something to be grasped" —
       "form" (morphE = essential nature/true form). "Grasped"
       (harpagmon = something to be clutched/exploited). WEB:
       "existing in the form of God, didn't consider equality with
       God a thing to be grasped." He didn't cling to His rights.

v.7  — NET: "but emptied himself by taking on the form of a
       slave" — "emptied" (ekenOsen = kenosis). WEB: "emptied
       himself, taking the form of a servant." KJV: "made himself
       of no reputation." What did He empty Himself OF? Not deity
       but the independent exercise of divine prerogatives.

v.9  — NET: "God exalted him and gave him the name that is above
       every name" — "the name" (to onoma = THE name). WEB: "God
       also highly exalted him." KJV: "God also hath highly exalted
       him." The name is "Lord" (kyrios, v.11) — the divine name
       (Yahweh in the LXX).

v.12 — NET: "work out your own salvation with fear and trembling"
       — "work out" (katergazesthe = bring to completion/carry to
       its goal). WEB: "work out your own salvation with fear and
       trembling." Not work FOR salvation but work OUT what God has
       worked IN (v.13: "God works in you")."""

notes[3] = """v.8  — NET: "I have suffered the loss of all things, and I
       regard them as dung, in order that I may gain Christ" —
       "dung" (skybalon = refuse/excrement/garbage). WEB: "count
       them nothing but refuse." KJV: "I count them but dung." The
       strongest term Paul could use — his Jewish resume is not
       merely worthless but repulsive compared to Christ.

v.10 — NET: "My aim is to know him, to experience the power of
       his resurrection, to share in his sufferings" — "know"
       (gnOnai = experiential, intimate knowing). WEB: "that I may
       know him, and the power of his resurrection." KJV: "That I
       may know him." Not information but union — resurrection
       power and suffering fellowship together.

v.12 — NET: "Not that I have already attained this... but I press
       on" — "press on" (diOkO = pursue/chase/hunt). WEB: "I press
       on." KJV: "I press toward the mark." Athletic/hunting
       imagery — single-minded, relentless forward pursuit.

v.14 — NET: "I press on toward the goal for the prize of the
       upward call of God in Christ Jesus" — "upward call" (anO
       klEseOs = heavenly/above calling). WEB: "the prize of the
       high calling of God in Christ Jesus." KJV: "the prize of
       the high calling." Not looking back, not looking around —
       only forward and upward.

v.20 — NET: "But our citizenship is in heaven" — "citizenship"
       (politeuma = commonwealth/colony). WEB: "our citizenship is
       in heaven." KJV: "our conversation is in heaven." Philippi
       was a Roman colony — citizens of Rome living far from Rome.
       Believers are heaven's colony on earth."""

notes[4] = """v.4  — NET: "Rejoice in the Lord always. Again I say, rejoice!"
       — "always" (pantote) — not when circumstances permit but
       always. Written from PRISON. WEB: "Rejoice in the Lord
       always! Again I will say, 'Rejoice!'" The repetition is
       deliberate — not a suggestion but a command.

v.6  — NET: "Do not be anxious about anything. Instead, in every
       situation, through prayer and petition with thanksgiving,
       tell your requests to God" — "anxious" (merimnate = be
       distracted by worry). WEB: "In nothing be anxious." KJV:
       "Be careful for nothing." The antidote to anxiety: prayer +
       thanksgiving.

v.7  — NET: "And the peace of God that surpasses all
       understanding will guard your hearts and minds in Christ
       Jesus" — "guard" (phrourEsei = garrison/stand sentry over —
       military term). WEB: "the peace of God... will guard your
       hearts." God's peace as an armed guard over the mind and
       emotions.

v.8  — NET: "whatever is true, whatever is worthy of respect,
       whatever is just, whatever is pure, whatever is lovely,
       whatever is commendable" — six virtues for mental focus.
       WEB: "whatever things are true... honorable... just... pure
       ...lovely... of good report." KJV: "whatsoever things are
       true." Mental discipline — choose what occupies your mind.

v.13 — NET: "I am able to do all things through the one who
       strengthens me" — "all things" (panta) in context = 
       contentment in all circumstances (v.12: abundance and need).
       WEB: "I can do all things through Christ, who strengthens
       me." KJV: "I can do all things through Christ which
       strengtheneth me." Often quoted out of context — it's about
       contentment, not unlimited ability."""


def add_additional_notes(filepath, notes_text):
    with open(filepath, 'r') as f:
        content = f.read()
    if 'ADDITIONAL TRANSLATION NOTES' in content:
        return False
    if 'GLOSSARY' in content:
        insertion_point = 'GLOSSARY'
    elif 'PERSONAL REFLECTION' in content:
        insertion_point = 'PERSONAL REFLECTION'
    else:
        return False
    block = "ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)\n------------------------------------\n" + notes_text.strip() + "\n\n"
    content = content.replace(insertion_point, block + insertion_point)
    with open(filepath, 'w') as f:
        f.write(content)
    return True

for ch, note_text in sorted(notes.items()):
    filepath = os.path.join(base, "Chapter " + str(ch), "Chapter " + str(ch) + " - Study Notes.txt")
    if os.path.isfile(filepath):
        if add_additional_notes(filepath, note_text):
            print("  done Chapter " + str(ch))
        else:
            print("  skip Chapter " + str(ch))
    else:
        print("  missing Chapter " + str(ch))
