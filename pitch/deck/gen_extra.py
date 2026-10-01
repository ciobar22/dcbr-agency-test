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
{moment('06', T('Õhtu','The evening'), T('Väsinud? Pirukas ootab.','Tired? A pie is waiting.'), T('Ei tea, mida süüa? Mõne minutiga on soe pirukas laual – ja tunned end kodus ja armastatuna.','Don’t know what to eat? A few minutes and a warm pie is on the table – and you feel at home and loved.'))}
</div>''', extra=";gap:36px"))

# CAMPAIGN EXECUTION
addslide("campaign_run", sec("campaign_run", f'''{head(T('Kampaania · kus see elab','Campaign · where it lives'), T('Üks lugu, igas kontaktpunktis.','One story, at every touchpoint.'))}
<div style="display:flex;gap:48px;align-items:start">
<div style="flex:1;display:flex;flex-direction:column;gap:18px">
{card(T('Karbi kaane sees','Inside the lid'), T('„Tere tulemast koju.“ + kaart „Kelle laud see on?“ – jaga oma pidulauda.','“Welcome home.” + a card “Whose table is this?” – share your feast table.'))}
{card(T('Trammid ja bussipeatused','Trams and bus stops'), T('Õhtune plakat: „Väsinud? Pirukas ootab.“','Evening poster: “Tired? A pie is waiting.”'))}
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
{fmt2('03', T('„Õhtune päästja“','“The evening rescue”'), T('Kell 18: väsinud? AIR fritüüri, mõne minutiga on õhtusöök valmis.','6 pm: tired? AIR into the fryer, dinner is ready in minutes.'), "#C9D99A")}
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


# DIRECTIONS A vs B
def dircol(tag, name, k1, k2, txt, rec=False):
    badge = f'<p style="font-size:24px;font-weight:700;color:{LIGHT};background:{BLUE};padding:6px 18px;border-radius:999px">{T("Soovitame","Recommended")}</p>' if rec else ''
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
            f'<div style="display:flex;gap:16px;align-items:center"><p style="{FD};font-size:40px;font-weight:600;color:{HEAD}">{tag} · {name}</p>{badge}</div>'
            f'<div style="display:flex;gap:16px">{img(k1,400,300,16,name)}{img(k2,400,300,16,name)}</div>'
            f'<p style="font-size:26px;line-height:1.4">{txt}</p></div>')
addslide("directions", sec("directions", f"""{head(T('Kaks visuaalset suunda','Two visual directions'), T('Pidulik punane-kuld või soe põhjamaine.','Festive red-gold or warm Nordic.'))}
<div style="display:flex;gap:48px">
{dircol('A', 'Pidu', 'mbA', 'packA', T('Must karp, kuldsed viljapead, punane kiri. Väga pidulik – sobib jõulu- ja kingiväljaandeks.','Black box, golden wheat, red script. Very festive – ideal for a Christmas and gift edition.'))}
{dircol('B', T('Põhjamaine','Nordic'), 'mbB', 'packB', T('Kaerakreem, rukkilill, kootud muster. Soe, kohalik, igapäevane – põhisari.','Oat cream, cornflower, woven pattern. Warm, local, everyday – the core range.'), True)}
</div>""", extra=";gap:32px"))

# IDENTITY SHEET full image
addslide("identity_sheet", f"""<section id="identity_sheet" data-transition="fade" style="background:#EFE6D6;color:{BODY};font-family:'DM Sans', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;gap:28px">
<div style="display:flex;flex-direction:column;gap:12px"><p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{BLUE}">{T('Brändi identiteet','Brand identity')}</p>
<h2 style="{FD};font-size:56px;font-weight:500;line-height:1.1;color:{HEAD}">{T('Logo, värvid, kiri ja muster – üks süsteem.','Logo, colours, type and pattern – one system.')}</h2></div>
<img src="{IMG['idB']}" alt="{T('Pirogoffi brändi identiteedi leht','Pirogoff brand identity sheet')}" style="width:1664px;height:620px;object-fit:contain;border-radius:20px">
{footer(0)}</section>""")

# LINEUP full-bleed
addslide("lineup", f"""<section id="lineup" data-transition="fade" style="background:{DARK};color:{LIGHT};font-family:'DM Sans', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column">
<img src="{IMG['lineup']}" alt="{T('GO, AIR ja KLASSIK formaadid','GO, AIR and KLASSIK formats')}" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover">
<div style="position:absolute;left:0px;top:0px;width:1920px;height:320px;background:linear-gradient(180deg, rgba(46,33,23,0.92) 0%, rgba(46,33,23,0) 100%)"></div>
<div style="position:absolute;left:128px;top:96px;width:1600px;display:flex;flex-direction:column;gap:12px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{LBLUE}">{T('Uued formaadid','New formats')}</p>
<h2 style="{FD};font-size:64px;font-weight:500;line-height:1.1;color:{LIGHT}">{T('Väike, keskmine, suur – igaks hetkeks oma pirukas.','Small, medium, large – a pie for every moment.')}</h2></div>
</section>""")

# FORMATS with images
def fcard(k, name, w, price, txt, col):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:20px">'
            f'{img(k,368,276,14,name)}<div style="display:flex;flex-direction:column;gap:8px;padding:8px 12px">'
            f'<p style="{FD};font-size:44px;font-weight:600;color:{HEAD}">{name}</p><p style="font-size:26px;font-weight:700;color:{col}">{w} · {price}</p>'
            f'<p style="font-size:24px;line-height:1.35">{txt}</p></div></div>')
addslide("formats2", sec("formats2", f"""{head(T('Formaadid','Formats'), T('Pirukas igaks hetkeks.','A pie for every moment.'))}
<div style="display:flex;gap:20px">
{fcard('go','GO','120 g','3,50 €',T('Käes söödav, paberümbrises. Tudengile ja reisijale.','Hand-held, in a paper sleeve. For students and commuters.'),TERRA)}
{fcard('tukk','TÜKK',T('viil','slice'),'2,90 €',T('Viil karbis kohvikutele ja letile.','A boxed slice for cafés and counters.'),"#5F7D50")}
{fcard('air','AIR','350 g',T('külmutatud','frozen'),T('Õhufritüüris mõne minutiga. Sügavkülmast õhtusöögiks.','A few minutes in the air fryer. Freezer to dinner.'),BLUE)}
{fcard('klassik','KLASSIK','1 kg',T('värske või külm.','fresh or frozen'),T('Pidulaua pirukas – küpseta kodus lõpuni.','The feast pie – finish baking at home.'),"#6B4A2B")}
</div>""", bg=ALT, extra=";gap:36px"))

# PERSONAS with student image
pp2=[(T('Tudeng','Student'),T('GO teel loengusse, alla 4 €.','GO on the way to class, under €4.')),(T('Pendelrändaja','Commuter'),T('Hommikune GO teel tööle.','A morning GO on the way to work.')),(T('Vanaema ja lapselaps','Grandma and grandchild'),T('Kaks GO-d jalutuskäigul.','Two GOs on a walk.')),(T('Pere','Family'),T('KLASSIK pühapäeva õhtusöögiks.','KLASSIK for Sunday dinner.')),(T('Kohvikukülastaja','Café guest'),T('Viil kohvi kõrvale.','A slice with their coffee.')),(T('Turist','Tourist'),T('Kohalik maitse kingikarbis.','A local taste in a gift box.'))]
def pcard(a,b):
    return (f'<div style="display:flex;flex-direction:column;gap:8px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:16px;padding:24px">'
            f'<h3 style="{FD};font-size:34px;font-weight:600;color:{HEAD}">{a}</h3><p style="font-size:26px;line-height:1.35">{b}</p></div>')
addslide("personas2", sec("personas2", f"""{head(T('Kellele','Who it is for'), T('Kuus inimest, kuus põhjust osta.','Six people, six reasons to buy.'))}
<div style="display:flex;gap:40px;align-items:start">
{img('student',500,620,24,T('Tudeng sööb GO pirukat vanalinnas','Student eating a GO pie in the Old Town'))}
<div style="flex:1;display:grid;grid-template-columns:repeat(2, 1fr);gap:20px">{''.join(pcard(a,b) for a,b in pp2)}</div>
</div>""", extra=";gap:36px"))


# ===== v4 compact slides =====
addslide("intro3", sec("intro3", f'''{head(T('Pirogoff täna','Pirogoff today'), T('Pirukad, mida armastatakse.<br>Nüüd on aeg, et neid leitaks.','Pies people love.<br>Now it is time to be found.'))}
<div style="display:flex;gap:48px;align-items:start">
{img('01b', 720, 540, 24, T('Kana ja puravikuga pirukas','Chicken and porcini pie'))}
<div style="flex:1;display:grid;grid-template-columns:repeat(2, 1fr);gap:24px">
{big('13 / 13', T('Facebooki arvustust soovitavad – „nagu vanaema tehtud“','Facebook reviews recommend it – “like grandma made”'), BLUE)}
{big('31+', T('käsitsi tehtud pirukat, küpsetatud iga päev Tiskres','handmade pies, baked daily in Tiskre'), TERRA)}
{big('4', T('müügiletti Rimi ja Prisma hüpermarketites + e-pood ja Wolt','counters in Rimi and Prisma hypermarkets + online shop and Wolt'), HEAD)}
{big('2023', T('viimane Instagrami postitus – aeg uuesti alustada','your last Instagram post – time to start again'), "#9C1449")}
</div></div>'''))

addslide("digital2", sec("digital2", f'''{head(T('Kus on kasv','Where the growth is'), T('Iga kanal on täna võimalus.','Every channel is an opportunity today.'))}
<table style="font-size:28px;color:{BODY};width:1664px">
<tr><th style="width:22%">{T('Kanal','Channel')}</th><th style="width:28%">{T('Täna','Today')}</th><th style="width:50%">{T('Võimalus','Opportunity')}</th></tr>
<tr><td>Instagram</td><td>183 · {T('viimane postitus 2023','last post 2023')}</td><td><b><span style="color:{BLUE}">{T('3 videoformaati, 3–4 postitust nädalas','3 video formats, 3–4 posts a week')}</span></b></td></tr>
<tr style="background:#FBF7F0"><td>Google Maps</td><td>0 {T('arvustust','reviews')}</td><td><b><span style="color:{BLUE}">{T('Profiil igale letile + arvustuskaart karbis','A profile per counter + review card in the box')}</span></b></td></tr>
<tr><td>Wolt / Bolt</td><td>{T('Wolt ilma hinnanguteta, Bolt puudub','Wolt without ratings, no Bolt')}</td><td><b><span style="color:{BLUE}">{T('Fotod, hinnangud, Bolt Food avada','Photos, ratings, switch on Bolt Food')}</span></b></td></tr>
<tr style="background:#FBF7F0"><td>{T('Koduleht','Website')}</td><td>{T('1. koht „pirukad Tallinn“','#1 for “pirukad Tallinn”')}</td><td><b><span style="color:{BLUE}">{T('Inglise keel + „tellimine“ ja „kohaletoimetamine“','English + “order” and “delivery” searches')}</span></b></td></tr>
<tr><td>B2B</td><td>{T('puudub','none yet')}</td><td><b><span style="color:{TERRA}">{T('Kohvikud ja supermarketid – suurim kasvuallikas','Cafés and supermarkets – the biggest growth source')}</span></b></td></tr>
</table>''', bg=ALT))

def aud(t,b): return (f'<div style="flex:1;display:flex;flex-direction:column;gap:8px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:16px;padding:28px">'
    f'<h3 style="{FD};font-size:34px;font-weight:600;color:{HEAD}">{t}</h3><p style="font-size:26px;line-height:1.35">{b}</p></div>')
addslide("market2", sec("market2", f'''{head(T('Turg ja publik','Market and audience'), T('Suur linn, kolm publikut.','A big city, three audiences.'))}
<div style="display:flex;gap:48px">
{big('460 584', T('elanikku Tallinnas','residents in Tallinn'), HEAD)}
{big('3,42 mln', T('välisturisti aastas','foreign visitors a year'), BLUE)}
{big('2 488 €', T('keskmine brutopalk Harjumaal','average gross wage, Harju'), TERRA)}
</div>
<div style="display:flex;gap:24px">
{aud(T('Püsikliendid','Regulars'), T('Venekeelsed tallinlased (~34%), kes tunnevad pirogi.','Russian-speaking locals (~34%) who know the pirog.'))}
{aud(T('Eestlased','Estonians'), T('Pirukas on ka eesti traditsioon – eesti keel esikohal.','The pirukas is Estonian too – Estonian first.'))}
{aud(T('Turistid','Tourists'), T('Kohalik maitse ja ilus karp kaasa võtmiseks.','A local taste and a beautiful box to take home.'))}
</div>''', extra=";gap:40px"))

addslide("compet2", sec("compet2", f'''{head(T('Konkurents','Competition'), T('Nõudlus on tõestatud. Koht on vaba.','Demand is proven. The space is free.'))}
<div style="display:flex;gap:48px">
<div style="width:620px;display:flex;flex-direction:column;gap:16px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:40px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{FOOT}">Nikolay · {T('sama toode, 30–38 €/kg','same product, €30–38/kg')}</p>
<p style="{FD};font-size:80px;font-weight:600;line-height:1;color:{TERRA}">17 828</p><p style="font-size:28px">{T('hinnangut Bolt Foodis','ratings on Bolt Food')}</p>
<p style="{FD};font-size:80px;font-weight:600;line-height:1;color:{TERRA}">1 981</p><p style="font-size:28px">{T('arvustust Google’is','reviews on Google')}</p>
</div>
<table style="font-size:28px;color:{BODY};width:996px">
<tr><th style="width:44%">{T('Ettevõte','Company')}</th><th style="width:56%">{T('Käive · fookus','Revenue · focus')}</th></tr>
<tr><td>Eesti Pagar</td><td>106,8 mln € · {T('tööstuslik','industrial')}</td></tr>
<tr style="background:#FBF7F0"><td>Leibur</td><td>29,9 mln € · {T('leib, jaekett','bread, retail')}</td></tr>
<tr><td>Pagaripoisid</td><td>3,55 mln € · {T('9 kohvikut','9 cafés')}</td></tr>
<tr style="background:#FBF7F0"><td>Nikolay, Nostalgia</td><td>{T('kodused pirukad tellimisel','homemade pies to order')}</td></tr>
</table></div>
<p style="font-size:28px;line-height:1.45">{T('Keegi ei oma veel positsiooni „käsitsi tehtud pidupirukas igas formaadis“.','Nobody yet owns “handmade feast pie in every format”.')}</p>''', bg=ALT))

def opp(icon, t, b):
    return (f'<div style="display:flex;gap:20px;align-items:start;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:16px;padding:28px">'
            f'<x-icon name="{icon}" style="color:{BLUE};width:52px;height:52px"></x-icon>'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:6px"><h3 style="{FD};font-size:34px;font-weight:600;color:{HEAD}">{t}</h3><p style="font-size:26px;line-height:1.35">{b}</p></div></div>')
addslide("opps", sec("opps", f'''{head(T('Võimalused','Opportunities'), T('Kasv tuleb B2B-st ja uutest formaatidest.','Growth comes from B2B and new formats.'))}
<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:20px">
{opp('Users', T('Kohvikud ja supermarketid','Cafés and supermarkets'), T('Viilud, GO ja KLASSIK kohalike tootjate riiulil.','Slices, GO and KLASSIK on the local producers’ shelf.'))}
{opp('Home', T('Külmutatud sari','Frozen range'), T('AIR ja KLASSIK: supermarketi sügavkülm ja Wolt Market.','AIR and KLASSIK: supermarket freezer and Wolt Market.'))}
{opp('Star', T('Kingikarp','Gift box'), T('Turistidele: sadam ja lennujaam, 11,5 mln reisijat.','For tourists: port and airport, 11.5 M passengers.'))}
{opp('Clock', T('Pühade sari','Holiday range'), T('Jõulud, lihavõtted, jaanipäev – eeltellimused.','Christmas, Easter, Midsummer – pre-orders.'))}
{opp('CheckCircle', T('Nädala pirukas','Pie of the week'), T('Tellimus: igal reedel uus maitse koju.','Subscription: a new flavour home every Friday.'))}
{opp('Globe', T('Soome ja Baltikum','Finland and the Baltics'), T('„Northern Feast Pies“ järgmise sammuna.','“Northern Feast Pies” as the next step.'))}
</div>''', extra=";gap:36px"))

addslide("b2b2", sec("b2b2", f'''{head('B2B', T('Pirogoff igas kohvikus ja supermarketis.','Pirogoff in every café and supermarket.'))}
<table style="font-size:28px;color:{BODY};width:1664px">
<tr><th style="width:30%">{T('Klient','Buyer')}</th><th style="width:40%">{T('Mida pakume','What we offer')}</th><th style="width:30%">{T('Tarne','Delivery')}</th></tr>
<tr><td>{T('Kohvikud ja kohvikuketid','Cafés and café chains')}</td><td>{T('Soolased TÜKK-viilud ja GO','Savoury TÜKK slices and GO')}</td><td>{T('Iga päev, jahutatud','Daily, chilled')}</td></tr>
<tr style="background:#FBF7F0"><td>{T('Supermarketid (Selver, Coop, Rimi, Prisma)','Supermarkets (Selver, Coop, Rimi, Prisma)')}</td><td>{T('Kohalike tootjate riiul: viilud, KLASSIK, AIR','Local producers’ shelf: slices, KLASSIK, AIR')}</td><td>{T('2–3× nädalas / külmutatult','2–3× a week / frozen')}</td></tr>
<tr><td>Wolt Market</td><td>{T('AIR ja KLASSIK külmutatult','AIR and KLASSIK frozen')}</td><td>{T('Kord nädalas','Weekly')}</td></tr>
</table>
<div style="display:flex;gap:24px">
{big('~215 €', T('laborianalüüs retsepti kohta (LABRIS)','lab analysis per recipe (LABRIS)'), BLUE)}
{big('2–4 p', T('säilivus jahutatult – või külmutatult','shelf life chilled – or frozen'), TERRA)}
{big('ET + GS1', T('eestikeelne märgistus ja vöötkood','Estonian labels and barcode'), HEAD)}
</div>''', bg=ALT))

ph2=[(T('0–30 päeva','0–30 days'),T('Korda','Tidy up'),T('Google’i profiilid, Bolt Food, Wolt, kõik sotsiaalmeedia lehed, koduleht.','Google profiles, Bolt Food, Wolt, every social page, website.')),
    (T('1–3 kuud','1–3 months'),T('Testi','Test'),T('Viilud ja GO olemasolevatel lettidel. Balti Jaama Turu analüüs.','Slices and GO at the existing counters. Balti Jaama Turg analysis.')),
    (T('3–6 kuud','3–6 months'),T('B2B','B2B'),T('Kohvikud ja supermarketid, uus pakend, labor ja märgistus.','Cafés and supermarkets, new packaging, lab and labels.')),
    (T('6–12 kuud','6–12 months'),T('Kasva','Grow'),T('Külmutatud sari. Kesklinna minipood ainult siis, kui B2B seda vajab.','Frozen range. A central mini-shop only if B2B needs it.'))]
rm2=""
for i,(a,b,c) in enumerate(ph2):
    col=[TERRA,"#B85F1C",BLUE,"#5F7D50"][i]
    rm2 += (f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF7F0;border:1px solid #E0D3BE;border-top:12px solid {col};border-radius:20px;padding:32px">'
           f'<p style="font-size:24px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{col}">{a}</p>'
           f'<h3 style="{FD};font-size:44px;font-weight:600;color:{HEAD}">{b}</h3><p style="font-size:26px;line-height:1.4">{c}</p></div>')
addslide("roadmap2", sec("roadmap2", f'''{head(T('Teekaart','Roadmap'), T('Alustame olemasolevatest punktidest.','We start from the existing points.'))}
<div style="display:flex;gap:20px">{rm2}</div>
<p style="font-size:28px;line-height:1.45;width:1560px">{T('Kui B2B töötab, pole kallist kesklinna asukohta vaja: vähem üüri, rohkem raha turundusse ja tootmisse.','If B2B works, an expensive central location is not needed: less rent, more money for marketing and production.')}</p>'''))

addslide("goals2", sec("goals2", f'''{head(T('12 kuu eesmärgid','12-month goals'), T('Kuhu jõuame aastaga.','Where we get to in a year.'))}
<div style="display:flex;gap:48px">
<div style="flex:3;display:grid;grid-template-columns:repeat(2, 1fr);gap:24px">
{big('165 000 €', T('käive – tagasi 2022. aasta tasemele ja edasi','revenue – back to the 2022 level and beyond'), BLUE)}
{big('300+', T('hinnangut Woltis ja Bolt Foodis','ratings on Wolt and Bolt Food'), TERRA)}
{big('5–10', T('püsivat B2B klienti','regular B2B clients'), HEAD)}
{big('6', T('aktiivset sotsiaalmeedia kanalit','active social channels'), "#5F7D50")}
</div>
<div style="flex:2;display:flex;flex-direction:column;gap:16px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:36px">
<h3 style="{FD};font-size:40px;font-weight:600;color:{HEAD}">{T('Toetused','Grants')}</h3>
<ul style="font-size:26px;line-height:1.5"><li>{T('EIS arendusvautšer kuni 35 000 €','EIS development voucher up to €35,000')}</li><li>{T('PRIA toiduainetööstus 15–50%','PRIA food industry 15–50%')}</li><li>{T('Tallinna digitoetus kuni 6 000 €/a','Tallinn digital grant up to €6,000/yr')}</li></ul>
</div></div>''', bg=ALT))


def focus(sid, k, n, name, tag, facts, rows, col):
    fr="".join(f'<div style="display:flex;flex-direction:column;gap:4px"><p style="font-size:24px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{col}">{a}</p><p style="font-size:28px;line-height:1.4;color:{BODY}">{b}</p></div>' for a,b in rows)
    addslide(sid, f"""<section id="{sid}" data-transition="fade" style="background:{OAT};color:{BODY};font-family:'DM Sans', Arial, sans-serif;padding:128px 128px 160px 1000px;display:flex;flex-direction:column;justify-content:center;gap:28px">
<img src="{IMG[k]}" alt="{name}" style="position:absolute;left:0px;top:0px;width:900px;height:1080px;object-fit:cover">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{col}">{T('Formaat','Format')} {n} / 4</p>
<h2 style="{FD};font-size:120px;font-weight:600;line-height:1;color:{HEAD}">{name}</h2>
<p style="{FD};font-size:44px;font-style:italic;line-height:1.2;color:{HEAD}">{tag}</p>
<p style="font-size:32px;font-weight:700;color:{col}">{facts}</p>
<div style="display:flex;flex-direction:column;gap:20px">{fr}</div>
{footer(0)}</section>""")

focus("f_go","go",1,"GO",T('Pirukas, mis mahub pihku.','A pie that fits in your hand.'),'120 g · 3,50 €',
 [(T('Kellele','For whom'),T('Tudengid, tööle minejad, vanaema ja lapselaps jalutuskäigul.','Students, people on the way to work, grandma and grandchild on a walk.')),
  (T('Kus','Where'),T('Olemasolevad letid, kohvikud, Wolt ja Bolt Food.','Existing counters, cafés, Wolt and Bolt Food.')),
  (T('Miks','Why'),T('Väike ostukogus toob uued kliendid, kes terve piruka järele ei tuleks.','A small purchase brings new customers who would not buy a whole pie.'))],TERRA)
focus("f_tukk","tukk",2,"TÜKK",T('Proovi enne, kui ostad terve.','Try it before you buy a whole one.'),T('viil · 2,90 €','slice · €2.90'),
 [(T('Kellele','For whom'),T('Kohvikukülastaja, kes võtab kohvi kõrvale midagi soolast.','The café guest who wants something savoury with their coffee.')),
  (T('Kus','Where'),T('Kohvikud ja kohvikuketid, supermarketi valmistoidu riiul.','Cafés and café chains, the supermarket ready-food shelf.')),
  (T('Miks','Why'),T('Lihtsaim B2B toode: karbis, sildiga, iga päev värske.','The easiest B2B product: boxed, labelled, fresh every day.'))],"#5F7D50")
focus("f_air","air",3,"AIR",T('Sügavkülmast õhtusöögiks.','From the freezer to dinner.'),T('350 g · külmutatud · õhufritüürile','350 g · frozen · for the air fryer'),
 [(T('Kellele','For whom'),T('Väsinud õhtu, kui ei tea, mida süüa – soe pirukas mõne minutiga.','The tired evening when you don’t know what to eat – a warm pie in minutes.')),
  (T('Kus','Where'),T('Supermarketi sügavkülm ja Wolt Market.','The supermarket freezer and Wolt Market.')),
  (T('Miks','Why'),T('Pikk säilivus, vähem raiskamist, tarne kord nädalas.','Long shelf life, less waste, weekly delivery.'))],BLUE)
focus("f_klassik","klassik2",4,"KLASSIK",T('Pidulaua pirukas – küpseta kodus lõpuni.','The feast pie – finish baking at home.'),T('1 kg · värske või külmutatud','1 kg · fresh or frozen'),
 [(T('Kellele','For whom'),T('Pühad, sünnipäevad, perekokkutulekud.','Holidays, birthdays, family gatherings.')),
  (T('Kus','Where'),T('E-pood, letid, supermarketi sügavkülm.','Online shop, counters, supermarket freezer.')),
  (T('Miks','Why'),T('Tänane põhitoode uues elus: ahjust laua peale, soe ja lõhnav.','Today’s core product in a new life: from the oven to the table, warm and fragrant.'))],"#6B4A2B")

FINAL=["cover","intro3","revenue","digital2","market2","compet2","prices","opps",
 "campaign","moments","campaign_run",
 "directions","identity","flavours","collection","shelf","lineup","formats2","f_go","f_tukk","f_air","f_klassik","personas2",
 "social2","connect","b2b2","roadmap2","goals2","next"]
