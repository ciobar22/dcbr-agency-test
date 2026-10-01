# --- extra / replacement slides (exec'd inside gen.py) ---
def addslide(sid, html): slides.append((sid, html))
def sec(sid, inner, bg=OAT, dark=False, extra=""):
    col = LIGHT if dark else BODY
    return (f'<section id="{sid}" data-transition="fade" style="background:{bg};color:{col};font-family:\'DM Sans\', Arial, sans-serif;'
            f'padding:128px 128px 160px;display:flex;flex-direction:column;gap:48px{extra}">{inner}{footer(0, dark)}</section>')

# INTRO (replaces story/name/company/today/product)
addslide("intro", sec("intro", f'''{head(T('Pirogoff täna','Pirogoff today'), T('Pirukad, mida armastatakse.<br>Nüüd on aeg, et neid leitaks.','Pies people love.<br>Now it is time to be found.'))}
<div style="display:flex;gap:48px;align-items:start">
{img('01b', 720, 540, 24, T('Kana ja puravikuga pirukas','Chicken and porcini pie'))}
<div style="flex:1;display:grid;grid-template-columns:repeat(2, 1fr);gap:24px">
{big('13 / 13', T('Facebooki arvustust soovitavad – „nagu vanaema tehtud“','Facebook reviews recommend it – “like grandma made”'), BLUE)}
{big('31+', T('käsitsi tehtud pirukat, küpsetatud iga päev Tiskres','handmade pies, baked daily in Tiskre'), TERRA)}
{big('4', T('müügiletti Rimi ja Prisma hüpermarketites + e-pood ja Wolt','counters in Rimi and Prisma hypermarkets + online shop and Wolt'), HEAD)}
{big('1.', T('koht Google’is „pirukad Tallinn“','place on Google for “pirukad Tallinn”'), "#5F7D50")}
</div></div>'''))

# OPPORTUNITY: WHERE
def place(name, num, txt, col):
    return (f'<div style="display:flex;flex-direction:column;gap:10px;background:#FBF7F0;border:1px solid #E0D3BE;border-left:12px solid {col};border-radius:16px;padding:28px 32px">'
            f'<h3 style="{FD};font-size:36px;font-weight:600;color:{HEAD}">{name}</h3>'
            f'<p style="font-size:28px;font-weight:700;color:{col}">{num}</p><p style="font-size:26px;line-height:1.35">{txt}</p></div>')
addslide("where", sec("where", f'''{head(T('Võimalused · kus','Opportunities · where'), T('Kuus kohta, kus Tallinn juba liigub.','Six places where Tallinn is already on the move.'))}
<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:24px">
{place('Balti Jaama Turg', T('5,1 mln külastust/a','5.1 M visits/yr'), T('Mikrolett 1–30 päeva: test enne lepingut.','Micro-stall for 1–30 days: test before signing.'), TERRA)}
{place('Viru Keskus', T('~15 mln külastust/a','~15 M visits/yr'), T('Kiosk bussiterminali kõrval: GO ja viilud.','Kiosk by the bus terminal: GO and slices.'), BLUE)}
{place(T('Vanalinn ja jõuluturg','Old Town & Christmas market'), T('3,42 mln turisti/a','3.42 M tourists/yr'), T('Hooajalett ja kingikarp kaasa võtmiseks.','Seasonal stall and a gift box to take home.'), "#B85F1C")}
{place(T('Sadam ja lennujaam','Port & airport'), T('8 mln + 3,5 mln reisijat','8 M + 3.5 M passengers'), T('Kingikarp soomlastele ja turistidele.','Gift box for Finns and tourists.'), "#5F7D50")}
{place('Ülemiste City', T('ärilinnak + Rail Baltica 2028','business campus + Rail Baltica 2028'), T('Kontorite koosolekukastid ja lõunad.','Meeting boxes and lunches for offices.'), "#6B4A2B")}
{place(T('Ülikoolid','Universities'), T('TLÜ 7 237 tudengit + TalTech','TLU 7,237 students + TalTech'), T('GO alla 4 € – tudengi lõuna teel.','GO under €4 – a student lunch on the go.'), "#9C1449")}
</div>''', bg=ALT, extra=";gap:36px"))

# OPPORTUNITY: WHAT
def idea(icon, t, b):
    return (f'<div style="display:flex;gap:24px;align-items:start;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:16px;padding:28px">'
            f'<x-icon name="{icon}" style="color:{BLUE};width:56px;height:56px"></x-icon>'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:8px"><h3 style="{FD};font-size:34px;font-weight:600;color:{HEAD}">{t}</h3><p style="font-size:26px;line-height:1.35">{b}</p></div></div>')
addslide("what", sec("what", f'''{head(T('Võimalused · mida','Opportunities · what'), T('Uued tooted, uued tellijad, uued hetked.','New products, new buyers, new moments.'))}
<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:20px">
{idea('Star', T('Kingikarp','Gift box'), T('Kolm väikest pirukat ilusas karbis – turistidele, ettevõtetele, pühadeks.','Three small pies in a beautiful box – for tourists, companies, holidays.'))}
{idea('Users', T('Kontoripakk','Office pack'), T('Koosolekud, sünnipäevad, reedene kohv. Tellimine ühe klikiga.','Meetings, birthdays, Friday coffee. One-click ordering.'))}
{idea('Clock', T('Pühade sari','Holiday range'), T('Jõulud, lihavõtted, jaanipäev, koolilõpp – eeltellimused nädal ette.','Christmas, Easter, Midsummer, graduations – pre-orders a week ahead.'))}
{idea('Home', T('Külmutatud AIR ja KLASSIK','Frozen AIR and KLASSIK'), T('Sügavkülmast õhtusöögiks: Selver, Coop, Wolt Market.','From the freezer to dinner: Selver, Coop, Wolt Market.'))}
{idea('CheckCircle', T('Nädala pirukas','Pie of the week'), T('Tellimus: igal reedel uus maitse koju toodud.','Subscription: a new flavour delivered every Friday.'))}
{idea('Globe', T('Soome ja Baltikum','Finland and the Baltics'), T('„Northern Feast Pies“ – Helsingi ja Riia järgmise sammuna.','“Northern Feast Pies” – Helsinki and Riga as the next step.'))}
</div>''', extra=";gap:36px"))

# CAMPAIGN HERO
addslide("campaign", f'''<section id="campaign" data-transition="fade" style="background:{DARK};color:{LIGHT};font-family:'DM Sans', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;justify-content:center">
<img src="{IMG['01a']}" alt="{T('Pirukas karbis linasel laudlinal','Pie in its box on a linen cloth')}" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover">
<div style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;background:linear-gradient(90deg, rgba(46,33,23,0.95) 0%, rgba(46,33,23,0.85) 45%, rgba(46,33,23,0.1) 100%)"></div>
<div style="display:flex;flex-direction:column;gap:28px;width:960px">
<p style="font-size:24px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:{LBLUE}">{T('Kampaania','Campaign')}</p>
<h1 style="{FD};font-size:120px;font-weight:600;line-height:1.02;color:{LIGHT}">{T('Nagu lapsepõlves.','Just like when you were little.')}</h1>
<p style="{FD};font-size:48px;font-style:italic;line-height:1.2;color:{SOFT}">{T('Maitse, mis viib sind koju.','The taste that brings you home.')}</p>
<p style="font-size:30px;line-height:1.5;color:{SOFT}">{T('Samad maitsed, mis olid vanaema laual. Iga pidu, iga perekokkutulek, iga väsinud õhtu – pirukas on traditsioon, mis teeb olemise koduseks.','The same flavours that were on grandma’s table. Every celebration, every family gathering, every tired evening – the pie is a tradition that makes you feel at home.')}</p>
</div>
{footer(0, True)}
</section>''')

# CAMPAIGN MOMENTS
def moment(k, t, line, body):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:16px">{img(k,520,330,20,t)}'
            f'<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{BLUE}">{t}</p>'
            f'<h3 style="{FD};font-size:38px;font-weight:600;line-height:1.15;color:{HEAD}">{line}</h3>'
            f'<p style="font-size:26px;line-height:1.4">{body}</p></div>')
addslide("moments", sec("moments", f'''{head(T('Kampaania · kolm hetke','Campaign · three moments'), T('Pirukas peab olema traditsioon.','A pie should be a tradition.'))}
<div style="display:flex;gap:32px">
{moment('12', T('Pidu','The celebration'), T('Igal peol on pirukas.','Every party has a pie.'), T('Sünnipäev, jõulud, jaanipäev – laual on Pirogoff, nagu alati.','Birthdays, Christmas, Midsummer – Pirogoff is on the table, as always.'))}
{moment('03', T('Pere','The family'), T('Iga perekokkutulek.','Every family gathering.'), T('Sama maitse, mis vanaema laual. Nüüd sinu laual.','The same taste as on grandma’s table. Now on yours.'))}
{moment('06', T('Õhtu','The evening'), T('Väsinud? Pirukas ootab.','Tired? A pie is waiting.'), T('Ei tea, mida süüa? 18 minutit ja tunned end kodus ja armastatuna.','Don’t know what to eat? 18 minutes and you feel at home and loved.'))}
</div>''', extra=";gap:36px"))

# CAMPAIGN EXECUTION
addslide("campaign_run", sec("campaign_run", f'''{head(T('Kampaania · kus see elab','Campaign · where it lives'), T('Üks lugu, igas kontaktpunktis.','One story, at every touchpoint.'))}
<div style="display:flex;gap:48px;align-items:start">
<div style="flex:1;display:flex;flex-direction:column;gap:18px">
{card(T('Karbi kaane sees','Inside the lid'), T('„Tere tulemast koju.“ + kaart „Kelle laud see on?“ – jaga oma pidulauda.','“Welcome home.” + a card “Whose table is this?” – share your feast table.'))}
{card(T('Balti jaam ja trammid','Balti jaam and trams'), T('Õhtune plakat: „Väsinud? Pirukas ootab. 18 min.“','Evening poster: “Tired? A pie is waiting. 18 min.”'))}
{card(T('Sotsiaalmeedia ja Wolt','Social and Wolt'), T('Lugude sari vanavanematest ja peolaudadest, õhtune Wolti pakkumine kell 18.','Story series on grandparents and feast tables, a 6 pm Wolt offer.'))}
</div>
{img('07', 620, 620, 24, T('Porgandipirukas karbis','Carrot pie in its box'))}
</div>''', bg=ALT))

# SOCIAL: activate all pages
def plat(name, role, cad, col):
    return (f'<div style="display:flex;flex-direction:column;gap:10px;background:#FBF7F0;border:1px solid #E0D3BE;border-top:10px solid {col};border-radius:16px;padding:28px">'
            f'<h3 style="{FD};font-size:34px;font-weight:600;color:{HEAD}">{name}</h3><p style="font-size:26px;line-height:1.35">{role}</p>'
            f'<p style="font-size:24px;font-weight:700;color:{col}">{cad}</p></div>')
addslide("social2", sec("social2", f'''{head(T('Sotsiaalmeedia · kõik kanalid','Social · every channel'), T('Aktiveerime kõik lehed – iga kanal oma rolliga.','We activate every page – each with its own job.'))}
<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:20px">
{plat('Instagram', T('Ärikonto, Reels, lood. ET + RU + EN.','Business account, Reels, stories. ET + RU + EN.'), T('3–4 postitust nädalas','3–4 posts a week'), "#9C1449")}
{plat('TikTok', T('Uus konto: POV köögist, „Pirukas testis“.','New account: kitchen POV, “Pie on test”.'), T('3 videot nädalas','3 videos a week'), HEAD)}
{plat('Facebook', T('Kogukond, sündmused, arvustused, venekeelne publik.','Community, events, reviews, Russian-speaking audience.'), T('2 postitust nädalas','2 posts a week'), BLUE)}
{plat('Google Business', T('4 profiili – iga lett: fotod, kellaajad, arvustused.','4 profiles – every counter: photos, hours, reviews.'), T('Vastus igale arvustusele','Reply to every review'), "#5F7D50")}
{plat('Wolt + Bolt Food', T('Fotod, värvikoodiga menüü, hommikune avamine.','Photos, colour-coded menu, morning opening.'), T('Pakkumine iga nädal','Weekly offer'), TERRA)}
{plat('YouTube Shorts', T('Samad videod veel ühes kohas – ilma lisatööta.','The same videos in one more place – no extra work.'), T('Taaskasutus','Repurposed'), "#B85F1C")}
</div>''', extra=";gap:36px"))

# CONNECTION FORMATS
def fmt2(n, t, b, col):
    return (f'<div style="display:flex;flex-direction:column;gap:10px;background:#3D2D20;border:1px solid #5A4532;border-radius:16px;padding:28px">'
            f'<p style="{FD};font-size:44px;font-weight:600;color:{col}">{n}</p><h3 style="{FD};font-size:34px;font-weight:600;color:{LIGHT}">{t}</h3>'
            f'<p style="font-size:26px;line-height:1.35;color:{SOFT}">{b}</p></div>')
addslide("connect", sec("connect", f'''{head(T('Formaadid, mis loovad sidet','Formats that build connection'), T('Inimesed ei jälgi pagarit. Nad jälgivad lugusid.','People don’t follow a bakery. They follow stories.'), dark=True)}
<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:20px">
{fmt2('01', T('„Vanaema retsept“','“Grandma’s recipe”'), T('Vanavanemad räägivad oma pirukamälestusi kaamerasse.','Grandparents share their pie memories on camera.'), LBLUE)}
{fmt2('02', T('„Kelle laud see on?“','“Whose table is this?”'), T('Kliendid saadavad pidulaua fotod – parim saab kuu pirukad.','Customers send feast-table photos – the best wins a month of pies.'), "#E9A58F")}
{fmt2('03', T('„Õhtune päästja“','“The evening rescue”'), T('Kell 18: väsinud? AIR fritüüris, 18 minutit, õhtusöök valmis.','6 pm: tired? AIR in the fryer, 18 minutes, dinner is ready.'), "#C9D99A")}
{fmt2('04', T('„POV: pirukas sünnib“','“POV: a pie is born”'), T('Kell 5 Tiskre köögis – tainas, täidis, punutis, ahi.','5 am in the Tiskre kitchen – dough, filling, braid, oven.'), LBLUE)}
{fmt2('05', T('„Pirukas testis“','“Pie on test”'), T('Ausad arvustused kohalikelt loojatelt ja klientidelt.','Honest reviews by local creators and customers.'), "#E9A58F")}
{fmt2('06', T('„Pühade kalender“','“Holiday calendar”'), T('Iga püha oma pirukas – eeltellimuse loendur.','A pie for every holiday – a pre-order countdown.'), "#C9D99A")}
</div>''', bg=DARK, dark=True, extra=";gap:36px"))

# READY: B2B system + lab merged
addslide("ready", sec("ready", f'''{head(T('B2B valmisolek','B2B readiness'), T('Iga retsept alati sama – tõestatult ohutu.','Every recipe always the same – proven safe.'))}
<div style="display:flex;gap:48px">
<div style="flex:1;display:flex;flex-direction:column;gap:14px">
<p style="font-size:30px;line-height:1.5"><b>1.</b> {T('Standardiseeritud retseptid ja tehnilised kaardid','Standardised recipes and spec sheets')}</p>
<p style="font-size:30px;line-height:1.5"><b>2.</b> {T('Labor: toiteväärtus ja säilivus (LABRIS)','Lab: nutrition and shelf life (LABRIS)')}</p>
<p style="font-size:30px;line-height:1.5"><b>3.</b> {T('Märgistus eesti keeles + GS1 vöötkood','Estonian labels + GS1 barcode')}</p>
<p style="font-size:30px;line-height:1.5"><b>4.</b> {T('Jahutatult 2–4 päeva või külmutatult','Chilled 2–4 days or frozen')}</p>
<p style="font-size:30px;line-height:1.5"><b>5.</b> {T('Müügikaust ja proovikarbid','Sales kit and sample boxes')}</p>
</div>
<div style="width:620px;display:flex;flex-direction:column;gap:20px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:40px">
{big('~215 €', T('säilivusuuring retsepti kohta','shelf-life study per recipe'), BLUE)}
{big('243 €', T('täielik toiteväärtuse analüüs','full nutrition panel'), TERRA)}
<p style="font-size:24px;color:{FOOT}">{T('Hinnad ilma KM-ta, LABRIS','Prices excl. VAT, LABRIS')}</p>
</div></div>''', bg=ALT))

FINAL=["cover","intro","revenue","digital",
 "market","benchmark","competitors","prices","audiences",
 "opportunity","where","what",
 "campaign","moments","campaign_run",
 "positioning","identity","flavours","collection","shelf","premium","formats","personas",
 "social2","connect",
 "channels","b2b","ready",
 "roadmap","goals","next"]
