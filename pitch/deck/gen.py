import json, os, sys
LANG = sys.argv[1]  # et | en
ROOT = sys.argv[2]
IMG = json.loads(sys.argv[3])
def T(et, en): return et if LANG == "et" else en

OAT="#F4EDE1"; ALT="#EADFCB"; DARK="#2E2117"; HEAD="#3B2A1C"; BODY="#5C4A3A"; FOOT="#6E5A47"
BLUE="#3A5BA0"; TERRA="#A8482F"; LIGHT="#F4EDE1"; SOFT="#D9C9B2"; LBLUE="#A9BEEA"
FD="font-family:'Fraunces', Georgia, serif"
TOTAL = 30
slides = []
def footer(n, dark=False):
    c = SOFT if dark else FOOT
    return (f'<p style="position:absolute;left:128px;bottom:64px;width:1200px;font-size:24px;color:{c}">Pirogoff · {T("Tallinna pidupirukad","Tallinn feast pies")}</p>'
            f'<p style="position:absolute;right:128px;bottom:64px;width:200px;text-align:right;font-size:24px;color:{c}">@@N@@ / @@T@@</p>')
def head(eyebrow, title, dark=False, accent=None):
    a = accent or (LBLUE if dark else BLUE); h = LIGHT if dark else HEAD
    return (f'<div style="display:flex;flex-direction:column;gap:16px">'
            f'<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{a}">{eyebrow}</p>'
            f'<h2 style="{FD};font-size:72px;font-weight:500;line-height:1.1;color:{h}">{title}</h2></div>')
def slide(sid, inner, bg=OAT, dark=False, extra=""):
    n = len(slides)+1
    col = LIGHT if dark else BODY
    s = (f'<section id="{sid}" data-transition="fade" style="background:{bg};color:{col};font-family:\'DM Sans\', Arial, sans-serif;'
         f'padding:128px 128px 160px;display:flex;flex-direction:column;gap:48px{extra}">{inner}{footer(n, dark)}</section>')
    slides.append((sid, s))
def card(title, body, bg="#FBF7F0", border="#E0D3BE", tcol=HEAD, bcol=BODY, extra=""):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:{bg};padding:36px;border:1px solid {border};border-radius:20px{extra}">'
            f'<h3 style="{FD};font-size:40px;font-weight:600;line-height:1.15;color:{tcol}">{title}</h3>'
            f'<p style="font-size:28px;line-height:1.4;color:{bcol}">{body}</p></div>')
def big(num, label, col=TERRA, lcol=BODY):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:8px">'
            f'<p style="{FD};font-size:96px;font-weight:600;line-height:1;color:{col}">{num}</p>'
            f'<p style="font-size:28px;line-height:1.35;color:{lcol}">{label}</p></div>')
def img(key, w, h, r=20, alt=""):
    return f'<img src="{IMG[key]}" alt="{alt}" style="width:{w}px;height:{h}px;object-fit:cover;border-radius:{r}px">'

# 1 COVER
n=1
slides.append(("cover", f'''<section id="cover" data-transition="fade" style="background:{DARK};color:{LIGHT};font-family:'DM Sans', Arial, sans-serif;padding:128px;display:flex;flex-direction:column;justify-content:center">
<img src="{IMG['02a']}" alt="{T('Pirogoffi pirukakarp','Pirogoff pie box')}" style="position:absolute;left:880px;top:0px;width:1040px;height:1080px;object-fit:cover">
<div style="position:absolute;left:760px;top:0px;width:240px;height:1080px;background:linear-gradient(90deg, {DARK} 0%, rgba(46,33,23,0) 100%)"></div>
<div style="display:flex;flex-direction:column;gap:28px;width:720px">
<p style="font-size:24px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:{LBLUE}">{T('Brändi uuendus · ettepanek','Brand relaunch · proposal')}</p>
<h1 style="{FD};font-size:150px;font-weight:600;line-height:1;color:{LIGHT}">Pirogoff</h1>
<p style="{FD};font-size:44px;font-style:italic;line-height:1.2;color:{SOFT}">{T('Tallinna pidupirukad','Tallinn feast pies')}</p>
<p style="font-size:30px;line-height:1.45;color:{SOFT}">{T('Kuidas viia käsitsi tehtud pirukad rohkemate inimesteni: uus identiteet, uued formaadid ja uued müügikanalid.','How to bring handmade pies to many more people: a new identity, new formats and new sales channels.')}</p>
</div>
<p style="position:absolute;left:128px;bottom:64px;width:700px;font-size:24px;color:{SOFT}">{T('Oktoober 2026','October 2026')}</p>
</section>'''))

# 2 STORY
slide("story", f'''{head(T('Meie lugu ühe lausega','Our story in one sentence'), T('Pirukad, mida armastatakse.<br>Nüüd on aeg, et neid ka leitaks.','Pies people love.<br>Now it is time for people to find them.'))}
<div style="display:flex;gap:48px;align-items:stretch">
{big('13 / 13', T('Facebooki arvustust soovitavad Pirogoffi – maitse, rohke täidis, „nagu vanaema tehtud“.','Facebook reviews recommend Pirogoff – taste, generous filling, “just like grandma made”.'), BLUE)}
{big('0', T('arvustust Google’is. Inimesed, kes otsivad pirukaid, ei näe veel seda, mida püsikliendid juba teavad.','reviews on Google. People searching for pies cannot yet see what regulars already know.'), TERRA)}
{big('1.', T('koht Google’is otsingule „pirukad Tallinn“. Nimi on olemas – nüüd vajab see lava.','place on Google for “pirukad Tallinn”. The name is there – now it needs a stage.'), HEAD)}
</div>''')

# 3 NAME
slide("name", f'''{head(T('Nime taga','Behind the name'), T('Pir tähendab pidu.','Pir means feast.'))}
<div style="display:flex;align-items:center;gap:24px">
<div style="flex:1;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:32px;display:flex;flex-direction:column;gap:8px"><p style="{FD};font-size:56px;font-weight:600;color:{TERRA}">pir</p><p style="font-size:26px">{T('slaavi tüvi: pidusöök','Slavic root: banquet')}</p></div>
<x-shape kind="arrow-right" style="width:64px;height:32px;background:{BLUE}"></x-shape>
<div style="flex:1;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:32px;display:flex;flex-direction:column;gap:8px"><p style="{FD};font-size:56px;font-weight:600;color:{TERRA}">pirog</p><p style="font-size:26px">{T('suur täidisega pirukas','the large filled pie')}</p></div>
<x-shape kind="arrow-right" style="width:64px;height:32px;background:{BLUE}"></x-shape>
<div style="flex:1;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:32px;display:flex;flex-direction:column;gap:8px"><p style="{FD};font-size:56px;font-weight:600;color:{TERRA}">pirukas</p><p style="font-size:26px">{T('eesti keeles – ja soome keeles piirakka','in Estonian – piirakka in Finnish')}</p></div>
<x-shape kind="arrow-right" style="width:64px;height:32px;background:{BLUE}"></x-shape>
<div style="flex:1;background:{BLUE};border-radius:20px;padding:32px;display:flex;flex-direction:column;gap:8px"><p style="{FD};font-size:56px;font-weight:600;color:{LIGHT}">pidu</p><p style="font-size:26px;color:{LIGHT}">{T('iga pirukas on pidu','every pie is a feast')}</p></div>
</div>
<p style="font-size:32px;line-height:1.45;width:1400px">{T('Pirukas on ühine traditsioon slaavi ja läänemeresoome kultuurides. See annab Pirogoffile loo, mis kõnetab eestlast, venekeelset tallinlast, soomlast ja turisti ühtviisi.','The pie is a shared tradition across Slavic and Finnic cultures. It gives Pirogoff a story that speaks equally to Estonians, Russian-speaking locals, Finns and tourists.')}</p>''')

# 4 COMPANY
slide("company", f'''{head(T('Olukord täna','Where we stand'), T('Väike meeskond, tugev toode, valmis kasvuks.','A small team, a strong product, ready to grow.'))}
<div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:24px">
{card('2019', T('OÜ Pirogoff.ee asutati; müük käib alates 2021. aastast.','OÜ Pirogoff.ee founded; trading since 2021.'))}
{card('Tiskre', T('Oma köök, kus pirukad küpsetatakse iga päev käsitsi.','Own kitchen where pies are baked by hand every day.'))}
{card('31–33', T('erinevat pirukat: soolased ja magusad, pärmi- või murutainas.','different pies: savoury and sweet, yeast or shortcrust.'))}
{card('1–4', T('töötajat. Lihtne struktuur = kiired otsused.','people. A lean structure = fast decisions.'))}
</div>
<p style="font-size:30px;line-height:1.45;width:1500px">{T('Kõik, mida tugev bränd vajab, on juba olemas: retseptid, tootmine ja rahulolevad kliendid. Järgmine samm on muuta see nähtavaks ja kättesaadavaks.','Everything a strong brand needs is already here: recipes, production and happy customers. The next step is to make it visible and easy to buy.')}</p>''')

# 5 REVENUE CHART
vals=[("2021",59.3),("2022",168.0),("2023",164.8),("2024",133.5),("2025",132.3)]
bars=""
for y,v in vals:
    h=max(4,int(v/168*360)); c = BLUE if y=="2022" else "#C9B79C"
    lab = f"{v:.0f}k" if v>=1 else "–"
    bars += (f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:end;gap:12px">'
             f'<p style="font-size:26px;font-weight:700;color:{HEAD}">{lab}</p>'
             f'<div style="width:160px;height:{h}px;background:{c};border-radius:10px 10px 0 0"></div>'
             f'<p style="font-size:26px;color:{BODY}">{y}</p></div>')
slide("revenue", f'''{head(T('Müügitulu 2019–2025, €','Revenue 2019–2025, €'), T('2022 tõestas: nõudlus on olemas.','2022 proved it: the demand is there.'))}
<div style="display:flex;gap:64px;align-items:end">
<div style="flex:1;display:flex;align-items:end;gap:8px;height:480px;border-bottom:2px solid #C9B79C">{bars}</div>
<div style="width:520px;display:flex;flex-direction:column;gap:24px">
<p style="{FD};font-size:56px;font-weight:600;line-height:1.1;color:{BLUE}">168 000 €</p>
<p style="font-size:28px;line-height:1.4">{T('Ühe formaadi ja ilma turunduseta jõudis Pirogoff 2022. aastal 168 000 euroni. Praegune tase (132 000 €) näitab, kui palju kasvuruumi on.','With one format and no marketing, Pirogoff reached €168,000 in 2022. Today’s level (€132,000) shows how much room there is to grow.')}</p>
<p style="font-size:24px;color:{FOOT}">{T('Allikas: äriregister, majandusaasta aruanded','Source: Estonian business register, annual reports')}</p>
</div></div>''')

# 6 CHANNELS TODAY
slide("today", f'''{head(T('Kus Pirogoff täna müüb','Where Pirogoff sells today'), T('Neli kanalit – kõik valmis tugevamaks muutuma.','Four channels – all ready to get stronger.'))}
<div style="display:grid;grid-template-columns:repeat(2, 1fr);gap:24px">
{card(T('Letid hüpermarketites','Counters in hypermarkets'), T('Rimi Haabersti, Rimi Sõpruse, Tiskre ja Lasnamäe. Igapäevane liiklus on juba olemas.','Rimi Haabersti, Rimi Sõpruse, Tiskre and Lasnamäe. The daily footfall is already there.'))}
{card(T('E-pood','Online shop'), T('pirogoff.ee: tarne Tallinnas 6 €, üle 50 € tasuta. Detailne koostis ja allergeenid.','pirogoff.ee: delivery in Tallinn €6, free over €50. Detailed ingredients and allergens.'))}
{card('Wolt', T('4 asukohta. Järgmine samm: hinnangud, fotod ja hommikused lahtiolekuajad.','4 locations. Next step: ratings, photos and morning opening hours.'))}
{card(T('Telefon ja Bolt Food','Phone and Bolt Food'), T('Tellimused telefoni teel. Bolt Food on avamiseks valmis – sinna jõuab uus kliendirühm.','Orders by phone. Bolt Food is ready to switch on – it reaches a new group of customers.'))}
</div>''', bg=ALT)

# 7 PRODUCT TODAY
slide("product", f'''{head(T('Toode täna','The product today'), T('Üks suurepärane formaat. Ruumi on veel kolmele.','One great format. Room for three more.'))}
<div style="display:flex;gap:48px;align-items:center">
{img('01b', 760, 570, 24, T('Kana ja puravikuga pirukas','Chicken and porcini pie'))}
<div style="flex:1;display:flex;flex-direction:column;gap:28px">
{big('0,9–1 kg', T('terve pirukas – ideaalne peolauale ja perele.','whole pie – perfect for the table and the family.'), TERRA)}
{big('19–33 €', T('hind pirukale. Puudu on veel väike ostukogus: viil ja käes söödav pirukas.','price per pie. What is still missing is a small purchase: a slice and a hand-held pie.'), BLUE)}
</div></div>''')

# 8 DIGITAL
slide("digital", f'''{head(T('Digitaalne nähtavus','Digital visibility'), T('Suurim võimalus peitub internetis.','The biggest opportunity is online.'))}
<table style="font-size:30px;color:{BODY};width:1664px">
<tr><th style="width:34%">{T('Kanal','Channel')}</th><th style="width:22%">{T('Täna','Today')}</th><th style="width:44%">{T('Võimalus','Opportunity')}</th></tr>
<tr><td>Instagram</td><td>183 {T('jälgijat','followers')}</td><td>{T('Kolm korduvat videoformaati, 3–4 postitust nädalas','Three repeatable video formats, 3–4 posts a week')}</td></tr>
<tr style="background:#FBF7F0"><td>Facebook</td><td>955 {T('jälgijat','followers')}</td><td>{T('13 kiitvat arvustust – kasutada neid reklaamis','13 glowing reviews – use them in ads')}</td></tr>
<tr><td>Google Maps</td><td>0 {T('arvustust','reviews')}</td><td>{T('Profiil igale letile + arvustuskaart karbis','A profile for every counter + review card in the box')}</td></tr>
<tr style="background:#FBF7F0"><td>{T('Google’i otsing','Google search')}</td><td>{T('1. koht „pirukad Tallinn“','#1 for “pirukad Tallinn”')}</td><td>{T('Võita ka „pirukate tellimine“ ja „kohaletoimetamine“','Also win “order pies” and “pie delivery”')}</td></tr>
<tr><td>{T('Koduleht','Website')}</td><td>{T('ET + RU','ET + RU')}</td><td>{T('Ingliskeelne versioon 3,4 mln välisturistile','English version for 3.4 M foreign visitors')}</td></tr>
</table>''')

# 9 MARKET
slide("market", f'''{head(T('Turg','The market'), T('Tallinn on suur, külastatud ja armastab mugavust.','Tallinn is big, visited and loves convenience.'))}
<div style="display:flex;gap:48px">
{big('460 584', T('elanikku Tallinnas (1.1.2026).','residents in Tallinn (1 Jan 2026).'), HEAD)}
{big('3,42 mln', T('välisturisti aastas (2025).','foreign visitors a year (2025).'), BLUE)}
{big('2 488 €', T('keskmine brutopalk Harjumaal (II kv 2026).','average gross wage in Harju county (Q2 2026).'), TERRA)}
</div>
<p style="font-size:30px;line-height:1.45;width:1500px">{T('Pagaritoodete turg kasvab väärtuses ja just mugavates formaatides: külmutatud, käes söödav, tellitav. Täpselt seal, kuhu Pirogoffi uued formaadid sihivad.','The bakery market grows in value and precisely in convenient formats: frozen, hand-held, ordered online. Exactly where Pirogoff’s new formats are aimed.')}</p>
<p style="font-size:24px;color:{FOOT}">{T('Allikad: Statistikaamet, Visit Tallinn, Fazer Eesti aruanne / Nielsen','Sources: Statistics Estonia, Visit Tallinn, Fazer Eesti report / Nielsen')}</p>''', bg=ALT)

# 10 NIKOLAY
slide("benchmark", f'''{head(T('Tõestatud nõudlus','Proven demand'), T('Tallinlased tellivad kodused pirukad juba veebist.','Tallinn already orders homemade pies online.'))}
<div style="display:flex;gap:48px">
<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:40px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{FOOT}">{T('Sarnane pagar Tallinnas','A similar bakery in Tallinn')}</p>
<p style="{FD};font-size:80px;font-weight:600;line-height:1;color:{TERRA}">17 828</p><p style="font-size:28px">{T('hinnangut Bolt Foodis (4,82 ★)','ratings on Bolt Food (4.82 ★)')}</p>
<p style="{FD};font-size:80px;font-weight:600;line-height:1;color:{TERRA}">1 981</p><p style="font-size:28px">{T('arvustust Google’is (4,7 ★)','reviews on Google (4.7 ★)')}</p>
</div>
<div style="flex:1;display:flex;flex-direction:column;gap:24px;justify-content:center">
<p style="{FD};font-size:48px;font-weight:500;line-height:1.2;color:{HEAD}">{T('Sama hinnaklass (30–38 €/kg), sama toode.','Same price range (€30–38/kg), same product.')}</p>
<p style="font-size:30px;line-height:1.45">{T('Nikolay on näidanud, et kodused pirukad müüvad rakendustes tuhandetele. Pirogoffil on toode – puudu on vaid nähtavus ja hinnangud.','Nikolay has shown that homemade pies sell to thousands through the apps. Pirogoff has the product – only visibility and ratings are missing.')}</p>
</div></div>''')

# 11 COMPETITOR MAP
slide("competitors", f'''{head(T('Konkurentsimaastik','Competitive landscape'), T('Suured teevad mahtu. Pirogoff teeb pidu.','The big players make volume. Pirogoff makes feasts.'))}
<table style="font-size:28px;color:{BODY};width:1664px">
<tr><th style="width:30%">{T('Ettevõte','Company')}</th><th style="width:22%">{T('Käive','Revenue')}</th><th style="width:48%">{T('Fookus','Focus')}</th></tr>
<tr><td>Eesti Pagar</td><td>106,8 mln € (2025)</td><td>{T('Tööstuslik leib ja pirukad, kauplustes','Industrial bread and pastries, in stores')}</td></tr>
<tr style="background:#FBF7F0"><td>Leibur</td><td>29,9 mln € (2025)</td><td>{T('Leib ja saiad, jaekett','Bread and buns, retail')}</td></tr>
<tr><td>Pagaripoisid</td><td>3,55 mln € (2025)</td><td>{T('9 kohvikut, igapäevased pirukad','9 cafés, everyday pastries')}</td></tr>
<tr style="background:#FBF7F0"><td>Café Lyon</td><td>1,27 mln € (2024)</td><td>{T('Prantsuse kondiitritooted','French patisserie')}</td></tr>
<tr><td>Nikolay, Nostalgia, Ahjupala</td><td>{T('väikesed','small')}</td><td>{T('Kodused suured pirukad tellimisel','Large homemade pies to order')}</td></tr>
</table>
<p style="font-size:28px;line-height:1.45">{T('Keegi ei hõivа veel positsiooni „käsitsi tehtud pidupirukas, mida saab osta igas formaadis“. See koht on vaba.','Nobody yet owns the position “handmade feast pie, available in every format”. That space is free.').replace('hõivа','hõiva')}</p>''', bg=ALT)

# 12 PRICE PER KG
rows=[("Pirogoff",21,37,BLUE),("Nikolay",30,38,"#B9A88E"),("Nostalgia",17,25,"#B9A88E")]
pr=""
for name,a,b,c in rows:
    left=int(a/40*1100); w=int((b-a)/40*1100)
    pr += (f'<div style="display:flex;align-items:center;gap:32px"><p style="width:260px;font-size:30px;font-weight:700;color:{HEAD}">{name}</p>'
           f'<div style="position:relative;width:1100px;height:56px;background:#E6DAC6;border-radius:28px">'
           f'<div style="position:absolute;left:{left}px;top:0px;width:{w}px;height:56px;background:{c};border-radius:28px"></div></div>'
           f'<p style="width:220px;font-size:30px;color:{HEAD}">{a}–{b} €</p></div>')
slide("prices", f'''{head(T('Hind kilogrammi kohta','Price per kilogram'), T('Pirogoff on õigel tasemel – ja vahemik on lai.','Pirogoff is priced right – and the range is wide.'))}
<div style="display:flex;flex-direction:column;gap:36px">{pr}
<div style="display:flex;gap:32px"><p style="width:260px;font-size:24px"></p><div style="width:1100px;display:flex;justify-content:space-between"><p style="font-size:24px;color:{FOOT}">0 €</p><p style="font-size:24px;color:{FOOT}">20 €</p><p style="font-size:24px;color:{FOOT}">40 €/kg</p></div></div></div>
<p style="font-size:28px;line-height:1.45;width:1500px">{T('Väiksemad formaadid (viil 2,90 €, GO 3,50 €) toovad Pirogoffi hinna inimesteni, kes täna terve piruka järele ei tule.','Smaller formats (slice €2.90, GO €3.50) bring Pirogoff within reach of people who would not buy a whole pie today.')}</p>''')

# 13 AUDIENCES
slide("audiences", f'''{head(T('Kaks publikut, üks bränd','Two audiences, one brand'), T('Püsikliendid jäävad. Uued tulevad juurde.','Regulars stay. New customers join.'))}
<div style="display:flex;gap:24px">
{card(T('Püsikliendid','Regulars'), T('Venekeelsed tallinlased (~34% linnast), kes tunnevad pirogi traditsiooni ja kirjutavad juba täna kiitvaid arvustusi.','Russian-speaking locals (~34% of the city) who know the pirog tradition and already write glowing reviews.'))}
{card(T('Eestlased','Estonians'), T('Pirukas on ka eesti traditsioon. Eesti keel esikohal, kohalik lugu, käsitöö.','Pirukas is an Estonian tradition too. Estonian first, a local story, craft.'))}
{card(T('Turistid ja välismaalased','Tourists and expats'), T('3,4 mln külastajat aastas otsivad kohalikku maitset, mida kaasa võtta.','3.4 M visitors a year look for a local taste to take home.'))}
</div>
<p style="font-size:30px;line-height:1.45;width:1500px">{T('Uus identiteet räägib kõigiga: tähendus „pidu“, läänemeresoome mustrid ja eesti keel esikohal.','The new identity speaks to all of them: the meaning “feast”, Baltic-Finnic patterns and Estonian first.')}</p>''', bg=ALT)

# 14 OPPORTUNITY (dark statement)
slide("opportunity", f'''{head(T('Võimalus','The opportunity'), T('Toode on valmis. Nüüd ehitame selle ümber brändi.','The product is ready. Now we build a brand around it.'), dark=True)}
<div style="display:flex;gap:24px">
{card(T('1 · Formaadid','1 · Formats'), T('Viil, käes söödav GO, külmutatud AIR ja KLASSIK – iga hetke jaoks oma pirukas.','Slice, hand-held GO, frozen AIR and KLASSIK – a pie for every moment.'), bg="#3D2D20", border="#5A4532", tcol=LIGHT, bcol=SOFT)}
{card(T('2 · Nähtavus','2 · Visibility'), T('Uus pakend, Google, Wolt, Bolt ja Instagram – et pirukad oleksid leitavad.','New packaging, Google, Wolt, Bolt and Instagram – so the pies can be found.'), bg="#3D2D20", border="#5A4532", tcol=LIGHT, bcol=SOFT)}
{card(T('3 · Kanalid','3 · Channels'), T('Balti Jaama Turg, kohvikud, kontorid ja kaupluste riiulid – B2B kõrvuti B2C-ga.','Balti Jaama Turg, cafés, offices and store shelves – B2B alongside B2C.'), bg="#3D2D20", border="#5A4532", tcol=LIGHT, bcol=SOFT)}
</div>''', bg=DARK, dark=True)

# 15 POSITIONING
slide("positioning", f'''{head(T('Uus positsioneerimine','New positioning'), T('Üks nimi, kaks kirjeldust.','One name, two descriptors.'))}
<div style="display:flex;gap:32px">
<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:48px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{BLUE}">{T('Eesti','Estonia')}</p>
<p style="{FD};font-size:72px;font-weight:600;line-height:1;color:{HEAD}">Pirogoff</p>
<p style="{FD};font-size:40px;font-style:italic;color:{TERRA}">Tallinna pidupirukad</p>
<p style="font-size:28px;line-height:1.4">{T('Kohalik, käsitsi tehtud, Tallinnast. Eesti keel esikohal.','Local, handmade, from Tallinn. Estonian first.')}</p></div>
<div style="flex:1;display:flex;flex-direction:column;gap:20px;background:{BLUE};border-radius:20px;padding:48px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{LIGHT}">{T('Laienemine: Baltikum ja Soome','Expansion: Baltics and Finland')}</p>
<p style="{FD};font-size:72px;font-weight:600;line-height:1;color:{LIGHT}">Pirogoff</p>
<p style="{FD};font-size:40px;font-style:italic;color:{LIGHT}">Northern Feast Pies</p>
<p style="font-size:28px;line-height:1.4;color:{LIGHT}">{T('FI: Pohjolan juhlapiirakat · LV: Ziemeļu svētku pīrāgi','FI: Pohjolan juhlapiirakat · LV: Ziemeļu svētku pīrāgi')}</p></div>
</div>
<p style="{FD};font-size:44px;font-style:italic;color:{HEAD}">Pir = pidu. Every pie is a feast.</p>''')

# 16 IDENTITY
sw=[("#F4EDE1",T("Kaerakreem","Oat cream"),HEAD),("#6B4A2B",T("Rukkipruun","Rye brown"),LIGHT),("#3A5BA0",T("Rukkilill","Cornflower"),LIGHT),("#C8A27A","Kraft",HEAD)]
sws="".join(f'<div style="flex:1;display:flex;flex-direction:column;justify-content:end;gap:4px;height:220px;background:{c};border:1px solid #D6C7AF;border-radius:20px;padding:28px"><p style="font-size:28px;font-weight:700;color:{t}">{n}</p><p style="font-size:24px;color:{t}">{c}</p></div>' for c,n,t in sw)
slide("identity", f'''{head(T('Brändi identiteet','Brand identity'), T('Soe, käsitööline, põhjamaine.','Warm, crafted, Nordic.'))}
<div style="display:flex;gap:48px;align-items:start">
<div style="flex:1;display:flex;flex-direction:column;gap:32px">
<div style="display:flex;gap:20px">{sws}</div>
<div style="display:flex;flex-direction:column;gap:12px">
<p style="font-size:30px;line-height:1.45"><b>{T('Logo:','Logo:')}</b> {T('pehme seriifkiri „Pirogoff“ ja rukkiõis – leib, põld, käsitöö.','soft serif wordmark “Pirogoff” with a rye sprig – bread, field, craft.')}</p>
<p style="font-size:30px;line-height:1.45"><b>{T('Muster:','Pattern:')}</b> {T('üks kootud rahvamustri riba – põhjamaine, mitte ühe rahva oma.','one woven folk band – Nordic, not tied to one nation.')}</p>
<p style="font-size:30px;line-height:1.45"><b>{T('Materjal:','Material:')}</b> {T('matt kartong, ümar aken, nöör. Ilma plastlaminaadita (EL PPWR).','matte board, round window, string. No plastic lamination (EU PPWR).')}</p>
</div></div>
{img('12', 600, 450, 24, T('Pakend maasika ja ricottaga','Strawberry and ricotta pack'))}
</div>''')

# 17 FLAVOUR CODE
fl=[("01","Kana & puravik","#B5523B",T("Soolane","Savoury")),("02","Sealiha & kapsas","#8E2F25",T("Soolane","Savoury")),("03","Veiseliha","#5E1F2B",T("Soolane","Savoury")),("04","Lõhe & spinat","#1F4E79",T("Soolane","Savoury")),("05","Kapsas & muna","#5F7D50",T("Soolane","Savoury")),("06","Seened","#6B4A2B",T("Soolane","Savoury")),("07","Porgand","#B85F1C",T("Soolane","Savoury")),
    ("08","Mustikas","#3B3A7A",T("Magus","Sweet")),("09","Õun","#5E7F2A",T("Magus","Sweet")),("10","Moon","#3A3A40",T("Magus","Sweet")),("11","Mustsõstar & vanill","#5B2A5E",T("Magus","Sweet")),("12","Maasikas & ricotta","#B23A55",T("Magus","Sweet")),("13","Kirss & valge šokolaad","#A3122E",T("Magus","Sweet")),("14","Vaarikas & tume šokolaad","#9C1449",T("Magus","Sweet"))]
chips="".join(f'<div style="display:flex;flex-direction:column;gap:6px;background:{c};border-radius:16px;padding:20px 22px"><p style="font-size:24px;font-weight:700;color:{LIGHT}">Nº {n} · {f}</p><p style="font-size:24px;color:{LIGHT}">{nm}</p></div>' for n,nm,c,f in fl)
slide("flavours", f'''{head(T('Värvikood','Colour code'), T('Iga maitse oma värviga – äratuntav sekundiga.','Every flavour has its colour – recognised in a second.'))}
<div style="display:grid;grid-template-columns:repeat(7, 1fr);gap:16px">{chips}</div>
<p style="font-size:28px;line-height:1.45;width:1500px">{T('Number, nimi ja värv korduvad kaanel, külgedel, Woltis ja leti menüüs. Püsiklient tellib lihtsalt „numbri 02“.','Number, name and colour repeat on the lid, the sides, on Wolt and on the counter menu. Regulars simply order “number 02”.')}</p>''', bg=ALT)

# 18 COLLECTION
g=[('01b','Kana & puravik'),('02a','Sealiha & kapsas'),('03','Veiseliha'),('06','Seened'),('07','Porgand'),('12','Maasikas & ricotta')]
gal="".join(f'<div style="display:flex;flex-direction:column;gap:10px">{img(k,536,290,18,nm)}<p style="font-size:24px;font-weight:700;color:{HEAD}">{nm}</p></div>' for k,nm in g)
slide("collection", f'''{head(T('Pakend · kollektsioon','Packaging · the collection'), T('Üks karp, palju maitseid.','One box, many flavours.'))}
<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:24px">{gal}</div>''', extra=";gap:36px")

# 19 SHELF
slide("shelf", f'''<img src="{IMG['shelf']}" alt="{T('Pirogoffi karbid poeriiulil','Pirogoff boxes on a store shelf')}" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover">
<div style="position:absolute;left:0px;top:0px;width:1920px;height:300px;background:linear-gradient(180deg, rgba(46,33,23,0.92) 0%, rgba(46,33,23,0) 100%)"></div>
<div style="position:absolute;left:128px;top:96px;width:1600px;display:flex;flex-direction:column;gap:12px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{LBLUE}">{T('Pakend · riiulil','Packaging · on the shelf')}</p>
<h2 style="{FD};font-size:64px;font-weight:500;line-height:1.1;color:{LIGHT}">{T('Värvisammas, mida loeb kaugelt.','A column of colour you can read from afar.')}</h2></div>''', bg=DARK, dark=True)

# 20 PREMIUM IDEAS
slide("premium", f'''{head(T('Pakend · lisaideed','Packaging · further ideas'), T('Külmletis raamaturiiul, kaanel maitse kuju.','A bookshelf in the freezer, the flavour’s shape on the lid.'))}
<div style="display:flex;gap:32px">
<div style="flex:1;display:flex;flex-direction:column;gap:14px">{img('freezer',800,460,20,T('Külmutatud AIR-karbid','Frozen AIR boxes'))}<p style="font-size:26px;line-height:1.4"><b>AIR</b> – {T('õhukesed karbid nagu raamatuseljad: värv + maitse püstiselt.','slim boxes like book spines: colour + flavour upright.')}</p></div>
<div style="flex:1;display:flex;flex-direction:column;gap:14px">{img('windows',800,460,20,T('Maitse kujuga aknad','Flavour-shaped windows'))}<p style="font-size:26px;line-height:1.4"><b>{T('Kujuaknad','Shaped windows')}</b> – {T('seen, kala, õun, mustikas. Kingi- ja hooajaväljaanne.','mushroom, fish, apple, blueberry. Gift and seasonal edition.')}</p></div>
</div>''', extra=";gap:36px")

# 21 FORMATS
def fmt(name, w, price, txt, col):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:14px;background:#FBF7F0;border:1px solid #E0D3BE;border-top:12px solid {col};border-radius:20px;padding:36px">'
            f'<p style="{FD};font-size:56px;font-weight:600;color:{HEAD}">{name}</p><p style="font-size:28px;font-weight:700;color:{col}">{w} · {price}</p>'
            f'<p style="font-size:26px;line-height:1.4">{txt}</p></div>')
slide("formats", f'''{head(T('Uued formaadid','New formats'), T('Pirukas igaks hetkeks.','A pie for every moment.'))}
<div style="display:flex;gap:24px">
{fmt('GO','120 g','3,50 €',T('Käes söödav pirukas paberümbrises. Tudengile, reisijale, jalutajale.','Hand-held pie in a paper sleeve. For students, commuters, strollers.'),TERRA)}
{fmt('TÜKK',T('viil','slice'),'2,90 €',T('Viil karbis kohvikutele ja letile. Proovi enne, kui ostad terve.','A boxed slice for cafés and counters. Try it before buying a whole one.'),"#5F7D50")}
{fmt('AIR','350 g',T('külmutatud','frozen'),T('Väike pirukas õhufritüürile: 18 min, 180 °C. Kaupluse sügavkülm.','Small pie for the air fryer: 18 min, 180 °C. Supermarket freezer.'),BLUE)}
{fmt('KLASSIK','1 kg',T('värske või külmutatud','fresh or frozen'),T('Pidulaua pirukas – värskelt või ahjus lõpuni küpsetamiseks.','The feast pie – fresh, or to finish baking in the oven.'),"#6B4A2B")}
</div>''', bg=ALT)

# 22 PERSONAS
pp=[(T('Tudeng','Student'),T('GO teel loengusse, alla 4 €.','GO on the way to class, under €4.')),(T('Pendelrändaja','Commuter'),T('Hommikune pirukas Balti jaamas.','A morning pie at Balti jaam.')),(T('Vanaema ja lapselaps','Grandma and grandchild'),T('Kaks GO-d jalutuskäigul vanalinnas.','Two GOs on a walk in the Old Town.')),(T('Pere','Family'),T('KLASSIK pühapäeva õhtusöögiks.','KLASSIK for Sunday dinner.')),(T('Kontor','Office'),T('Pirukakast koosolekuks või sünnipäevaks.','A pie box for a meeting or birthday.')),(T('Turist','Tourist'),T('Kohalik maitse ja ilus karp kaasa.','A local taste and a beautiful box to take home.'))]
pc="".join(card(a,b) for a,b in pp)
slide("personas", f'''{head(T('Kellele','Who it is for'), T('Kuus inimest, kuus põhjust osta.','Six people, six reasons to buy.'))}
<div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:24px">{pc}</div>''')

# 23 CHANNELS NEW
slide("channels", f'''{head(T('Kanalid · B2C','Channels · B2C'), T('Olla seal, kus inimesed juba on.','Be where people already are.'))}
<div style="display:flex;gap:32px">
<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:40px">
<h3 style="{FD};font-size:44px;font-weight:600;color:{HEAD}">Wolt + Bolt Food</h3>
<ul style="font-size:28px;line-height:1.5"><li>{T('Bolt Foodi avamine – uus kliendirühm','Switch on Bolt Food – a new customer group')}</li><li>{T('Professionaalsed fotod ja värvikoodiga menüü','Professional photos and a colour-coded menu')}</li><li>{T('Hommikune avamine alates kl 8','Open from 8 am for breakfast')}</li><li>{T('Eesmärk: sajad hinnangud 12 kuuga','Goal: hundreds of ratings in 12 months')}</li></ul></div>
<div style="flex:1;display:flex;flex-direction:column;gap:16px;background:{BLUE};border-radius:20px;padding:40px">
<h3 style="{FD};font-size:44px;font-weight:600;color:{LIGHT}">Balti Jaama Turg</h3>
<ul style="font-size:28px;line-height:1.5;color:{LIGHT}"><li>{T('5,1 mln külastust aastas','5.1 M visits a year')}</li><li>{T('Mikroletid 1,2 × 1,2 m, 1–30 päeva','Micro-stalls 1.2 × 1.2 m, 1–30 days')}</li><li>{T('Testime enne, kui allkirjastame','We test before we sign')}</li><li>{T('Järgmisena: Viru Keskus, jõuluturg','Next: Viru Keskus, Christmas market')}</li></ul></div>
</div>''', bg=ALT)

# 24 B2B
slide("b2b", f'''{head(T('Kanalid · B2B','Channels · B2B'), T('Pirogoff igas kohvikus, kontoris ja kaupluses.','Pirogoff in every café, office and store.'))}
<table style="font-size:28px;color:{BODY};width:1664px">
<tr><th style="width:28%">{T('Klient','Buyer')}</th><th style="width:36%">{T('Mida pakume','What we offer')}</th><th style="width:36%">{T('Tarne','Delivery')}</th></tr>
<tr><td>{T('Kohvikud (nt Reval Café)','Cafés (e.g. Reval Café)')}</td><td>{T('Soolased TÜKK-viilud ja GO','Savoury TÜKK slices and GO')}</td><td>{T('Iga päev, jahutatud','Daily, chilled')}</td></tr>
<tr style="background:#FBF7F0"><td>{T('Kontorid','Offices')}</td><td>{T('Koosoleku- ja sünnipäevakast','Meeting and birthday box')}</td><td>{T('Tellimisel','To order')}</td></tr>
<tr><td>Selver, Coop</td><td>{T('Kohalike tootjate riiul','Local producers’ shelf')}</td><td>{T('2–3 korda nädalas','2–3 times a week')}</td></tr>
<tr style="background:#FBF7F0"><td>Rimi</td><td>{T('Pakendatud viilud lettide kõrval','Packed slices next to the counters')}</td><td>{T('Iga päev','Daily')}</td></tr>
<tr><td>Wolt Market</td><td>{T('AIR ja KLASSIK külmutatult','AIR and KLASSIK frozen')}</td><td>{T('Kord nädalas','Weekly')}</td></tr>
</table>''')

# 25 B2B SYSTEM
steps=[(T('Retseptid','Recipes'),T('Standardiseeritud tehnilised kaardid','Standardised spec sheets')),(T('Labor','Lab'),T('Toiteväärtus ja säilivus','Nutrition and shelf life')),(T('Märgistus','Labelling'),T('Eesti keeles, GS1 vöötkood','In Estonian, GS1 barcode')),(T('Tarne','Delivery'),T('Jahutatud 2–4 päeva või külmutatud','Chilled 2–4 days or frozen')),(T('Müük','Sales'),T('Müügikaust ja proovikarbid','Sales kit and sample boxes'))]
st=""
for i,(a,b) in enumerate(steps):
    st += (f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:32px">'
           f'<p style="{FD};font-size:56px;font-weight:600;color:{BLUE}">{i+1}</p><h3 style="{FD};font-size:36px;font-weight:600;color:{HEAD}">{a}</h3><p style="font-size:26px;line-height:1.4">{b}</p></div>')
slide("system", f'''{head(T('B2B süsteem','The B2B system'), T('Viis sammu iga ostja jaoks valmis.','Five steps to be ready for any buyer.'))}
<div style="display:flex;gap:20px">{st}</div>
<p style="font-size:28px;line-height:1.45;width:1500px">{T('Kiirelt riknevate toiduainete eest makstakse seaduse järgi kuni 30 päeva jooksul – rahavoog on ette planeeritav.','By law, perishable food is paid within 30 days at most – cash flow can be planned ahead.')}</p>''', bg=ALT)

# 26 LAB
slide("lab", f'''{head(T('Kvaliteet ja vastavus','Quality and compliance'), T('Iga retsept alati ühesugune – ja tõestatult ohutu.','Every recipe always the same – and proven safe.'))}
<div style="display:flex;gap:48px">
<table style="font-size:28px;color:{BODY};width:900px">
<tr><th style="width:62%">{T('Analüüs (LABRIS)','Test (LABRIS)')}</th><th style="width:38%">{T('Hind ilma KM-ta','Price excl. VAT')}</th></tr>
<tr><td>{T('Toiteväärtus, täispakett','Full nutrition panel')}</td><td>243 €</td></tr>
<tr style="background:#FBF7F0"><td>Listeria</td><td>19–22 €</td></tr>
<tr><td>{T('Pärmid ja hallitused','Yeasts and moulds')}</td><td>16 €</td></tr>
<tr style="background:#FBF7F0"><td>{T('Üldine mikroobide arv','Total viable count')}</td><td>13 €</td></tr>
<tr><td>pH</td><td>8 €</td></tr>
</table>
<div style="flex:1;display:flex;flex-direction:column;gap:24px">
{big('~215 €', T('säilivusuuring ühe retsepti kohta','shelf-life study per recipe'), BLUE)}
<p style="font-size:28px;line-height:1.45">{T('Soolased pirukad: jahutatult 2–4 päeva või külmutatult. Magusat sarja saab kohandada toatemperatuuril müügiks.','Savoury pies: chilled 2–4 days or frozen. The sweet range can be adapted for ambient sale.')}</p>
</div></div>''')

# 27 SOCIAL
slide("social", f'''{head(T('Sisu','Content'), T('Kolm korduvat formaati, mis ehitavad usaldust.','Three repeatable formats that build trust.'))}
<div style="display:flex;gap:24px">
{card(T('„POV: pirukas sünnib“','“POV: a pie is born”'), T('Kell 5 Tiskre köögis: tainas, täidis, punutis, ahi. 20–30-sekundiline video esimeses isikus.','5 am in the Tiskre kitchen: dough, filling, braid, oven. A 20–30 second first-person video.'))}
{card(T('„Pirukas testis“','“Pie on test”'), T('Ausa arvustuse sari: karbi avamine, lõige, esimene amps, hinne. Kliendid ja kohalikud loojad.','An honest review series: unboxing, the cut, first bite, the score. Customers and local creators.'))}
{card(T('„Pidupirukad“','“Feast pies”'), T('Lood laudadest: sünnipäevad, pühad, pere. Pir = pidu – iga pirukas on pidu.','Stories from tables: birthdays, holidays, family. Pir = feast – every pie is a feast.'))}
</div>
<p style="font-size:28px;line-height:1.45">{T('Rütm: 3–4 postitust nädalas · arvustuskaart igas karbis · Google’i profiil igale letile.','Rhythm: 3–4 posts a week · a review card in every box · a Google profile for every counter.')}</p>''', bg=ALT)

# 28 ROADMAP
ph=[(T('0–30 päeva','0–30 days'),T('Korda','Tidy up'),T('Google’i profiilid, Bolt Food, Wolt, Instagram, koduleht.','Google profiles, Bolt Food, Wolt, Instagram, website.')),
    (T('1–3 kuud','1–3 months'),T('Testi','Test'),T('Viilud ja GO lettidel, arvustuste kampaania, Balti Jaama Turg.','Slices and GO at the counters, review campaign, Balti Jaama Turg.')),
    (T('3–6 kuud','3–6 months'),T('B2B pilot','B2B pilot'),T('5–10 kohvikut ja kontorit, uus pakend, Selver ja Coop.','5–10 cafés and offices, new packaging, Selver and Coop.')),
    (T('6–12 kuud','6–12 months'),T('Kasva','Grow'),T('Püsiv kiosk, külmutatud sari AIR ja KLASSIK.','A permanent kiosk, the frozen AIR and KLASSIK range.'))]
rm=""
for i,(a,b,c) in enumerate(ph):
    col=[TERRA,"#B85F1C",BLUE,"#5F7D50"][i]
    rm += (f'<div style="flex:1;display:flex;flex-direction:column;gap:12px;background:#FBF7F0;border:1px solid #E0D3BE;border-top:12px solid {col};border-radius:20px;padding:32px">'
           f'<p style="font-size:24px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:{col}">{a}</p>'
           f'<h3 style="{FD};font-size:44px;font-weight:600;color:{HEAD}">{b}</h3><p style="font-size:26px;line-height:1.4">{c}</p></div>')
slide("roadmap", f'''{head(T('Teekaart','Roadmap'), T('Neli etappi, iga samm mõõdetav.','Four stages, every step measurable.'))}
<div style="display:flex;gap:20px">{rm}</div>''')

# 29 GOALS + GRANTS
slide("goals", f'''{head(T('12 kuu eesmärgid','12-month goals'), T('Kuhu jõuame aastaga.','Where we get to in a year.'))}
<div style="display:flex;gap:48px">
<div style="flex:3;display:grid;grid-template-columns:repeat(2, 1fr);gap:24px">
{big('165 000 €', T('käive – tagasi 2022. aasta tasemele ja edasi','revenue – back to the 2022 level and beyond'), BLUE)}
{big('300+', T('hinnangut Woltis ja Bolt Foodis','ratings on Wolt and Bolt Food'), TERRA)}
{big('5–10', T('püsivat B2B klienti','regular B2B clients'), HEAD)}
{big('2', T('testi: Balti Jaama Turg ja jõuluturg','tests: Balti Jaama Turg and Christmas market'), "#5F7D50")}
</div>
<div style="flex:2;display:flex;flex-direction:column;gap:16px;background:#FBF7F0;border:1px solid #E0D3BE;border-radius:20px;padding:36px">
<h3 style="{FD};font-size:40px;font-weight:600;color:{HEAD}">{T('Toetused','Grants')}</h3>
<ul style="font-size:26px;line-height:1.5"><li>{T('EIS arendusvautšer kuni 35 000 €','EIS development voucher up to €35,000')}</li><li>{T('EIS innovatsioonivautšer kuni 7 500 €','EIS innovation voucher up to €7,500')}</li><li>{T('PRIA toiduainetööstus 15–50%','PRIA food industry 15–50%')}</li><li>{T('Tallinna digitoetus kuni 6 000 €/a','Tallinn digital grant up to €6,000/yr')}</li></ul>
</div></div>''', bg=ALT)

# 30 CLOSE
slides.append(("next", f'''<section id="next" data-transition="fade" style="background:{DARK};color:{LIGHT};font-family:'DM Sans', Arial, sans-serif;padding:128px 128px 160px;display:flex;flex-direction:column;justify-content:center">
<img src="{IMG['02b']}" alt="{T('Pirogoffi pirukas karbis','Pirogoff pie in its box')}" style="position:absolute;left:1040px;top:0px;width:880px;height:1080px;object-fit:cover">
<div style="position:absolute;left:920px;top:0px;width:200px;height:1080px;background:linear-gradient(90deg, {DARK} 0%, rgba(46,33,23,0) 100%)"></div>
<div style="display:flex;flex-direction:column;gap:32px;width:780px">
<p style="font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:{LBLUE}">{T('Järgmised sammud','Next steps')}</p>
<h2 style="{FD};font-size:80px;font-weight:500;line-height:1.1;color:{LIGHT}">{T('Teeme igast pirukast peo.','Let’s make every pie a feast.')}</h2>
<ol style="font-size:30px;line-height:1.6;color:{SOFT}"><li>{T('Kohtumine ja tagasiside sellele ettepanekule','Meeting and feedback on this proposal')}</li><li>{T('Müügiandmed kanalite kaupa ja kulud','Sales data by channel and costs')}</li><li>{T('Start: esimesed 30 päeva','Kick-off: the first 30 days')}</li></ol>
</div>
<p style="position:absolute;left:128px;bottom:64px;width:700px;font-size:24px;color:{SOFT}">Pirogoff · {T('Tallinna pidupirukad','Tallinn feast pies')}</p>
<p style="position:absolute;left:760px;bottom:64px;width:200px;text-align:right;font-size:24px;color:{SOFT}">@@N@@ / @@T@@</p>
</section>'''))

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'gen_extra.py')).read())
os.makedirs(f"{ROOT}/project/slides", exist_ok=True)
for f in os.listdir(f"{ROOT}/project/slides"): os.remove(f"{ROOT}/project/slides/{f}")
D=dict(slides)
order=FINAL
for k,sid in enumerate(order):
    html=D[sid].replace('@@N@@',f'{k+1:02d}').replace('@@T@@',str(len(order)))
    open(f"{ROOT}/project/slides/{sid}.html","w").write(html)
deck={"v":4,"createdOnFiles":{"v":1,"at":"2026-10-01T12:00:00Z"},"lists":"css",
 "title":T("Pirogoff · Tallinna pidupirukad – ettepanek","Pirogoff · Tallinn feast pies – proposal"),
 "order":order,
 "sections":{"s1":{"description":T("Avamine ja olukord","Opening and where we stand"),"start":"cover"},
             "s2":{"description":T("Turg, konkurents ja võimalused","Market, competition and opportunities"),"start":"market2"},
             "s3":{"description":T("Kampaania „Nagu lapsepõlves“","Campaign “Just like when you were little”"),"start":"campaign"},
             "s4":{"description":T("Bränd, pakend ja formaadid","Brand, packaging and formats"),"start":"directions"},
             "s5":{"description":T("Sotsiaalmeedia ja B2B","Social media and B2B"),"start":"social2"},
             "s6":{"description":T("Plaan","Plan"),"start":"roadmap2"}},
 "faces":{"fraunces":{"family":"Fraunces","href":"https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,400..700;1,400..700&display=swap"},
          "dm-sans":{"family":"DM Sans","href":"https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap"}},
 "designSystems":[]}
json.dump(deck, open(f"{ROOT}/project/deck.json","w"), ensure_ascii=False, indent=1)
print(order)
