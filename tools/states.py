"""Generates states/*.html, the table of driving-hours-by-state.html and STATES in calc.js.

One list below is the source of truth for the web. Requirements: IIHS graduated licensing
table (April 2026). The first 25 match the app presets (Hourglass/Model/Goal.swift); the
others are web-only until the app gets them too.

Run from the repo root: python3 tools/states.py
"""
import json
import re

BASE = "https://komorebideuxiemedunom.github.io/hourglass-app/"
# id, name, total hours, night hours, months held (0 = none), note
S = [
    ("al", "Alabama", 50, 0, 6, ""), ("az", "Arizona", 30, 10, 6, ""), ("ca", "California", 50, 10, 6, ""),
    ("co", "Colorado", 50, 10, 12, ""), ("fl", "Florida", 50, 10, 12, ""), ("ga", "Georgia", 40, 6, 12, ""),
    ("il", "Illinois", 50, 10, 9, ""), ("in", "Indiana", 50, 10, 6, ""), ("ky", "Kentucky", 60, 10, 6, ""),
    ("la", "Louisiana", 50, 15, 6, ""), ("md", "Maryland", 60, 10, 9, ""), ("ma", "Massachusetts", 40, 0, 6, ""),
    ("mi", "Michigan", 50, 10, 6, ""), ("mn", "Minnesota", 50, 15, 6, ""), ("mo", "Missouri", 40, 10, 6, ""),
    ("ny", "New York", 50, 15, 6, ""), ("nc", "North Carolina", 60, 10, 12, ""), ("oh", "Ohio", 50, 10, 6, ""),
    ("pa", "Pennsylvania", 65, 10, 6, "Includes 5 hours in bad weather."), ("sc", "South Carolina", 40, 10, 6, ""),
    ("tn", "Tennessee", 50, 10, 6, ""), ("tx", "Texas", 30, 10, 6, ""), ("ut", "Utah", 40, 10, 6, ""),
    ("va", "Virginia", 45, 15, 9, ""), ("wa", "Washington", 50, 10, 6, ""),
    # Web-only (IIHS, April 2026)
    ("ak", "Alaska", 40, 10, 6, "The 10 night hours may also be driven in bad weather."),
    ("ar", "Arkansas", 50, 10, 6, "Arkansas sets no minimum: 50 hours with 10 at night is the usual recommendation."),
    ("ct", "Connecticut", 40, 0, 6, "4 months with the permit after driver education."),
    ("de", "Delaware", 50, 10, 6, ""),
    ("dc", "District of Columbia", 40, 0, 6, "10 night hours are required later, in the provisional stage."),
    ("hi", "Hawaii", 50, 10, 6, ""), ("id", "Idaho", 50, 10, 6, ""), ("ia", "Iowa", 20, 2, 12, ""),
    ("ks", "Kansas", 50, 10, 12, "25 hours during the learner phase and 25 more before age 16."),
    ("me", "Maine", 70, 10, 6, ""),
    ("ms", "Mississippi", 50, 10, 12, "Mississippi sets no hours minimum: 50 hours with 10 at night is the usual recommendation."),
    ("mt", "Montana", 50, 10, 6, ""),
    ("ne", "Nebraska", 50, 10, 6, "No hours required after driver education."),
    ("nv", "Nevada", 50, 10, 6, "No hours required after an approved defensive driving course."),
    ("nh", "New Hampshire", 40, 10, 0, ""), ("nj", "New Jersey", 50, 10, 6, ""), ("nm", "New Mexico", 50, 10, 6, ""),
    ("nd", "North Dakota", 50, 0, 12, "Applies under 16. At 16 or older: no hours, 6 months with the permit."),
    ("ok", "Oklahoma", 50, 10, 6, ""),
    ("or", "Oregon", 100, 0, 6, "50 hours with an approved driver education course."),
    ("ri", "Rhode Island", 50, 10, 6, ""),
    ("sd", "South Dakota", 50, 10, 9, "10 of the hours in bad weather; 6 months with driver education."),
    ("vt", "Vermont", 40, 10, 12, ""),
    ("wv", "West Virginia", 50, 10, 6, "No hours required after driver education."),
    ("wi", "Wisconsin", 50, 10, 6, ""), ("wy", "Wyoming", 50, 10, 0, ""),
]
NO_MINIMUM = {"ar", "ms"}
S.sort(key=lambda s: s[1])


def slug(name):
    return re.sub(r"[^a-z]+", "-", name.lower()).strip("-")


HOLD = {"wy": "10 days"}


def hold(months, sid=""):
    return HOLD.get(sid) or (f"{months} months" if months else "no minimum")


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


HEAD = open("states/utah.html").read().split("<title>")[0]


def page(sid, name, total, night, months, note):
    url = f"{BASE}states/{slug(name)}.html"
    others = " · ".join([f'<a href="../driving-hours-by-state.html">All states</a>'] +
                        [f'<a href="{slug(n)}.html">{n}</a>' for i, n, *_ in S if i != sid])
    none = sid in NO_MINIMUM
    night_txt = f", {night} of them at night" if night else ""
    if none:
        title = f"{name} Learner's Permit Driving Hours (2026): No Minimum, Calculator | Hourglass"
        desc = f"{name} sets no minimum of supervised driving hours with a learner's permit. Most families still aim for {total} hours, {night} at night. Free calculator: hours left and weekly pace."
        answer = f"{name} does not set a minimum number of supervised driving hours. Most driving instructors still recommend about {total} hours, {night} of them at night, before the road test."
        facts = f'<p><strong>No minimum</strong> of supervised hours</p><p><strong>{total} hours</strong> recommended</p><p><strong>{hold(months, sid)}</strong> holding the permit</p>'
        lead = f"{name} does not require a set number of practice hours, but the road test still comes. Enter what's done so far to see where you stand against the usual {total}-hour goal."
    else:
        title = f"{name} Learner's Permit Driving Hours (2026): {total} Hours, Calculator | Hourglass"
        held = months or sid in HOLD
        hold_d = f" and {hold(months, sid)} with the learner's permit" if held else ""
        desc = f"{name} requires {total} supervised driving hours{f' including {night} at night' if night else ''}{hold_d}. Free calculator: hours left and hours a week to be ready by the road test."
        held = months or sid in HOLD
        answer = f"{name} asks for {total} hours of supervised driving{night_txt}" + (f", and at least {hold(months, sid)} holding the permit before the road test." if held else ", with no minimum holding period for the permit.")
        facts = f'<p><strong>{total} hours</strong> of supervised driving</p>' + (f'<p><strong>{night} hours</strong> at night</p>' if night else "") + (f'<p><strong>{hold(months, sid)}</strong> holding the permit</p>' if months or sid in HOLD else "<p><strong>No minimum</strong> time with the permit</p>")
        lead = f"{name} teens need {total} hours of supervised practice{f', including {night} at night' if night else ''}" + (f", and at least {hold(months, sid)} with the learner's permit before the road test." if held else ", before the road test.") + " Enter what's done so far to see what's left and the weekly pace to be ready on time."
    if note and not none:
        answer += " " + note
        lead = lead.replace(" Enter what's", f" {note} Enter what's")
    span = months or 6
    pace = f"Spread over {span} months, {total} hours is about {fmt(total / (span * 4.33))} hours a week. The calculator above adjusts the pace to the hours already driven and your test date."
    faq = [(f"How many hours do you need to drive with a learner's permit in {name}?", answer),
           ("How many hours a week is that?", pace),
           ("What counts as night driving?", "Driving between sunset and sunrise. Hourglass counts it automatically from the real sunset and sunrise where each drive starts."),
           (f"Where do I check the official {name} rules?", f"On the {name} DMV (or Department of Public Safety) website. Requirements change, and some states lower the hours after driver education.")]
    ld_app = {"@context": "https://schema.org", "@type": "WebApplication", "name": f"{name} learner's permit hours calculator", "applicationCategory": "EducationalApplication", "operatingSystem": "Web", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": url}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return f"""{HEAD}<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}"><link rel="preload" href="../fonts/barlow-condensed-800.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="../style.css"><script src="../calc.js" defer></script>
<script type="application/ld+json">{json.dumps(ld_app, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script></head>
<body data-mode="us" data-state="{sid}"><main><a class="marque" href="../index.html"><img src="../icon.png" alt="">Hourglass</a>
<h1>{name} learner's permit: driving hours</h1>
<div class="card facts">{facts}</div>
<p>{lead}</p>
<form class="card" id="calc"><div class="fields">
<label>State<select id="state"></select></label>
<label>Hours already driven<input id="done" inputmode="decimal" value="0"></label>
<label>Night hours already driven<input id="night" inputmode="decimal" value="0"></label>
<label>Planned road test date<input id="test" type="date"></label>
</div><div id="result" aria-live="polite"></div></form>
<div class="cta"><p><strong>Logging every drive by hand is where hours get lost.</strong> Hourglass times each drive with one tap, counts night hours from real sunset and sunrise, and exports a clean PDF log to sign. On iPhone, no account, no ads.</p><a class="btn" href="https://apps.apple.com/app/id6818433938">Get Hourglass</a></div>
{"".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in faq)}
<p class="note">Requirements as published in 2026 (IIHS graduated licensing table). Always confirm on the official {name} website. Hourglass is a log book, not legal advice.</p>
<p>Prefer paper? <a href="../printable-driving-log.html">Free printable driving log</a>, set up for {name}.</p>
<h2>Other states</h2><p class="others">{others}</p>
<footer><a href="../index.html">Hourglass</a> · <a href="../privacy.html">Privacy</a> · © 2026 Lucas Dansac</footer></main></body></html>
"""


for sid, name, total, night, months, note in S:
    open(f"states/{slug(name)}.html", "w").write(page(sid, name, total, night, months, note))

# Table of the hub page.
rows = "".join(f'<tr><td><a href="states/{slug(n)}.html">{n}</a></td><td>{"none" if i in NO_MINIMUM else f"{t} h"}</td><td>{"n/a" if not ni or i in NO_MINIMUM else f"{ni} h"}</td><td>{hold(m, i)}</td></tr>'
               for i, n, t, ni, m, _ in S)
hub = open("driving-hours-by-state.html").read()
hub = re.sub(r"(<tbody>).*?(</tbody>)", lambda m: m.group(1) + rows + m.group(2), hub, count=1, flags=re.S)
open("driving-hours-by-state.html", "w").write(hub)

# STATES of calc.js.
data = [{"id": i, "name": n, "total": float(t), "night": float(ni), "months": m,
         "note": no or (f"The permit must be held at least {HOLD[i]}." if i in HOLD else "")} for i, n, t, ni, m, no in S]
calc = open("calc.js").read()
calc = re.sub(r"const STATES = \[.*?\];", "const STATES = " + json.dumps(data, ensure_ascii=False) + ";", calc, count=1, flags=re.S)
open("calc.js", "w").write(calc)

# Printable log: one <option> per state carries its requirement for log.js.
LOG = "printable-driving-log.html"
def option(i, n, t, ni):
    none = i in NO_MINIMUM
    return f'<option value="{i}" data-total="{t}" data-night="{0 if none else ni}"' + (' data-none="1"' if none else "") + f">{n}</option>"


opts = "".join(option(i, n, t, ni) for i, n, t, ni, *_ in S)
log_faq = [("Is there a free printable driving log for a learner's permit?", "Yes: pick your state above, add the student's name, and print it or save it as a PDF. Each row has the date, start and end time, minutes, night minutes, road and weather conditions, and the supervisor's initials."),
           ("Can I use this log instead of the DMV form?", "Some states accept any written log signed by a parent; others want their own form, sometimes at the road test or with driver education. Check your state's DMV website, and copy your totals onto the official form if one is required."),
           ("How do I count night hours?", "Night driving is between sunset and sunrise. Write the minutes driven after sunset in the night column: they count toward both the night requirement and the total."),
           ("Is there an easier way than paper?", "Hourglass times each drive with one tap on iPhone, counts night minutes from the real sunset and sunrise, and exports a clean PDF log to sign. No account, no ads.")]
log_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in log_faq]}
open(LOG, "w").write(f"""{HEAD}<title>Printable Driving Log for Learner's Permit (Free PDF, All 50 States) | Hourglass</title>
<meta name="description" content="Free printable supervised driving log for teens with a learner's permit: pick your state, print or save as PDF. Columns for date, time, night minutes, conditions and supervisor initials.">
<link rel="canonical" href="{BASE}{LOG}"><link rel="preload" href="fonts/barlow-condensed-800.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="style.css"><script src="log.js" defer></script>
<script type="application/ld+json">{json.dumps(log_ld, ensure_ascii=False)}</script></head>
<body><main><a class="marque" href="index.html"><img src="icon.png" alt="">Hourglass</a>
<h1>Printable driving log</h1>
<p>A free supervised driving log for learner's permit practice. Pick your state to print its hour requirement at the top, then print it or save it as a PDF.</p>
<form class="card" id="logForm"><div class="fields">
<label>State<select id="logState"><option value="">Any state</option>{opts}</select></label>
<label>Student name (optional)<input id="student" autocomplete="off"></label>
<label>Rows<select id="rows"><option>25</option><option selected>40</option><option>60</option></select></label>
</div><button type="button" id="print">Print or save as PDF</button></form>
<div id="sheet"></div>
<div class="cta"><p><strong>Paper logs get lost, and night minutes are easy to get wrong.</strong> Hourglass times each drive with one tap, counts night hours from real sunset and sunrise, and exports a clean PDF log to sign. On iPhone, no account, no ads.</p><a class="btn" href="https://apps.apple.com/app/id6818433938">Get Hourglass</a></div>
{"".join(f"<h2>{q}</h2><p>{a}</p>" for q, a in log_faq)}
<p><a href="driving-hours-by-state.html">Driving hours required in each state</a></p>
<footer><a href="index.html">Hourglass</a> · <a href="privacy.html">Privacy</a> · © 2026 Lucas Dansac</footer></main></body></html>
""")
# Sitemap.
sm = open("sitemap.xml").read()
for _, n, *_ in S:
    loc = f"{BASE}states/{slug(n)}.html"
    if loc not in sm:
        sm = sm.replace("</urlset>", f"<url><loc>{loc}</loc><lastmod>2026-10-23</lastmod></url></urlset>")
if f"{BASE}{LOG}" not in sm:
    sm = sm.replace("</urlset>", f"<url><loc>{BASE}{LOG}</loc><lastmod>2026-10-23</lastmod></url></urlset>")
open("sitemap.xml", "w").write(sm)
print(len(S), "states")
