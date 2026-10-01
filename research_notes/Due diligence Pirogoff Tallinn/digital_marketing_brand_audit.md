# Pirogoff (Tallinn): digital marketing performance and brand audit, with competitor benchmark

*How this was collected (all metrics are stamped **2026-10-01** unless another date is given):* pirogoff.ee, wolt.com, pagespeed.web.dev, the Apify API and the Instagram/Facebook CDNs were blocked by this environment's egress proxy, and the session's WebSearch quota was used up after one query. Almost all data therefore comes from Apify actors that fetch the public pages server-side. The actors used were: `apify/instagram-profile-scraper`, `apify/instagram-scraper` (Pirogoff capped at 30 posts), `apify/website-content-crawler` (48 pages of pirogoff.ee), `compass/crawler-google-places`, `apify/google-search-scraper` (google.ee, desktop, no geolocation, one page per query), `apify/facebook-pages-scraper`, `apify/facebook-posts-scraper`, `apify/facebook-reviews-scraper`, `apify/facebook-ads-scraper` (Meta Ad Library, country EE), `teodor_banea/wolt-…` and `teodor_banea/bolt-food-…` scrapers, `dev00/Google-PageSpeed-Insights-api`, `trovevault/e-commerce-tech-stack-detector` and `clockworks/tiktok-scraper`. Each citation below points to the public URL the data describes. Each section keeps **measured data** (Cited Findings) apart from **my judgement** (Inferences). No images could be viewed (CDN blocked), so the visual brand review is based on text, alt-text, file names and page structure only.

---

## 1. Instagram @pirogoff_tln and other social accounts: size, activity, engagement, content

### Takeaway
@pirogoff_tln is small (183 followers) and **dormant**: the last feed post was on 2023-12-17, about 33.5 months before this audit. Most of its activity came in Nov 2021–Jul 2022. That period's engagement relied on giveaways and promo codes, and almost no organic comments came in. Facebook (955 followers) is the only social channel still active, at only 2–3 posts a year. No TikTok, separate Russian-language account, VK or Telegram presence was found.

### Cited Findings
**Profile snapshot (2026-10-01)**
- @pirogoff_tln has **183 followers, follows 119 accounts, 43 posts, 5 story highlights, 2 IGTV/video items**. The display name is empty. The bio reads only "In Pie We Trust" with a link to https://pirogoff.ee/. It is **not set as a business account** (`isBusinessAccount: false`, no business category), so it has no contact/address buttons and no Insights. — [Instagram @pirogoff_tln](https://www.instagram.com/pirogoff_tln/)
- The account ID (50064842719) is in a range assigned around 2021. The Facebook page was created **13 June 2021**. — [Instagram @pirogoff_tln](https://www.instagram.com/pirogoff_tln/); [Facebook Pirogoff.ee](https://www.facebook.com/Pirogoff.ee)

**Posting history (30 most recent of 43 posts scraped)**
- **Most recent post: 2023-12-17**, a carousel announcing sponsorship of the student film "Eyes of the Past" (Baltic Film, Media and Arts School). It got 4 likes and 0 comments. — [IG post C09278rChTl](https://www.instagram.com/p/C09278rChTl/)
- The post before that was 2023-02-23, a Solaris mall pop-up announcement in English (16 likes, 1 comment). — [IG post CpAqT_6ttjE](https://www.instagram.com/p/CpAqT_6ttjE/)
- **Oldest post in the 30-post sample: 2021-11-25**, a beef pie post (21 likes). The remaining 13 older posts were not scraped (30-post cap), so the exact first-post date is unknown. It is probably mid/late 2021 (see Gaps). — [IG post CWsisPINTh4](https://www.instagram.com/p/CWsisPINTh4/)
- Posts per year in the sample: **2021: 16 (13 of them in Dec 2021), 2022: 12, 2023: 2, 2024–2026: 0**. By month: Nov-21 3, Dec-21 13, Jan-22 3, Feb-22 2, Mar-22 2, Apr-22 1, May-22 1, Jun-22 2, Jul-22 1, Feb-23 1, Dec-23 1. — [Instagram @pirogoff_tln](https://www.instagram.com/pirogoff_tln/)
- Formats in the 30-post sample: **16 single images, 12 carousels, 2 short videos** (5–6 s, IGTV/reel type, 81 and 120 views). No Reels in the modern sense have been posted since 2022. — [IG video Celyya3LkG7](https://www.instagram.com/p/Celyya3LkG7/); [IG video CXGYr79Leg-](https://www.instagram.com/p/CXGYr79Leg-/)

**Engagement (30-post sample; follower base = 183 on 2026-10-01)**
- Mean likes **16.3** (median 15). Mean comments **11.7**, but the median is **0**: one giveaway post holds 344 of the 352 comments. — [IG post CbiL4pOtyUj](https://www.instagram.com/p/CbiL4pOtyUj/)
- The best post was the 2021-11-26 giveaway (62 likes). Without the two giveaway posts, mean likes are 13.9 and mean comments 0.29. — [IG post CWwLX-qNhM6](https://www.instagram.com/p/CWwLX-qNhM6/)
- Calculated engagement rate, (likes + comments) / current followers: **15.3%** with all posts and **7.7%** without the two giveaways. For the last 12 posts (Jan 2022–Dec 2023) excluding the giveaway it is 6.9%. My calculation; see Inferences for why these figures overstate current health. — [Instagram @pirogoff_tln](https://www.instagram.com/pirogoff_tln/)

**Languages, hashtags, promotions, UGC, collaborations**
- Caption languages (30 posts, my manual classification): **18 Estonian only, 8 bilingual Russian + Estonian, 1 Russian only, 2 English only, 1 without a caption**. Bilingual posts include the giveaways and new-product launches. — [IG post CfzMF5NNybJ](https://www.instagram.com/p/CfzMF5NNybJ/); [IG post CaUeCmSt37j](https://www.instagram.com/p/CaUeCmSt37j/)
- Hashtags appear on only **3 of 30** posts: #giveaway #tallinn #eesti #loosimäng #pirukas #toit #food #seenepirukas #puravikud #pirogoff #pirukad #pies. — [IG post CW8QD_HtgMw](https://www.instagram.com/p/CW8QD_HtgMw/); [IG post CpAqT_6ttjE](https://www.instagram.com/p/CpAqT_6ttjE/)
- Giveaways: **Nov 2021** (5 blackcurrant pies; tag a friend, share, follow IG + FB), **Jan 2022** (5 pies, run on Facebook only) and **Mar 2022** (3 pies, 344 comments). — [IG post CWwLX-qNhM6](https://www.instagram.com/p/CWwLX-qNhM6/); [IG post CY_binUNQd3](https://www.instagram.com/p/CY_binUNQd3/); [IG post CbiL4pOtyUj](https://www.instagram.com/p/CbiL4pOtyUj/)
- Promo codes: **blackcurrant25** (25% off, valid to 19.12.2021, a consolation prize for giveaway entrants) and **DEAL20** (20% off all pies on the web shop, to 28.02.2022). — [IG post CXEKuPqtLdZ](https://www.instagram.com/p/CXEKuPqtLdZ/); [IG post CaUfJakt96L](https://www.instagram.com/p/CaUfJakt96L/)
- The only collaboration found is the Dec 2023 film sponsorship. No paid-partnership flags appear on any scraped post, and no influencer or brand co-posts were found. — [IG post C09278rChTl](https://www.instagram.com/p/C09278rChTl/)
- No customer reposts (UGC) appear in the scraped feed. The tagged-photos tab was not scraped (see Gaps). — [Instagram @pirogoff_tln](https://www.instagram.com/pirogoff_tln/)
- Captions contain a data error: the shop phone is printed as "+372 960 950" (digits missing) on several posts, while the correct number "+37255960950" appears elsewhere. — [IG video Celyya3LkG7](https://www.instagram.com/p/Celyya3LkG7/); [IG post CfzMF5NNybJ](https://www.instagram.com/p/CfzMF5NNybJ/)

**Other accounts**
- **Facebook page "Pirogoff.ee | Tallinn"**: 955 followers, category "Product/service", price range "$$". The intro reads "Käsitsi ja armastusega tehtud pirukad!" (handmade pies made with love). The address on file is still **Ülemiste keskus, Suur-Sõjamäe 4**. It has 13 reviews (100% recommend) and showed the label "This Page is currently running ads". — [Facebook Pirogoff.ee](https://www.facebook.com/Pirogoff.ee)
- The most recent Facebook posts were on 2026-07-24 (summer sale, ET + EN, 3 likes, 2 shares), 2026-07-24 (image, 1 like), 2026-02-08 (Russian, 4 likes), 2025-01-25 (English, 5 likes), 2024-06-14 (English, 6 likes) and 2024-04-06 (English post with 7 likes plus a reel with 208 views). The film-sponsorship post on 2023-12-15 had 19 likes and 7 shares. — [FB post 2026-07-24](https://www.facebook.com/Pirogoff.ee/posts/pfbid036tFZmbuiU22QXrwuSEtXXyqybuTdDLUxYEHqwNmwbHXzhksZvvFJ42T9s2fLGF2ml); [FB post 2025-01-25](https://www.facebook.com/Pirogoff.ee/posts/pfbid02UrWwEnhKxQAYrd9mBmfXgBCnTDiYRnf2AGJT5MDrKMxjEoYSuq5KwmUewaWFapmdl); [FB reel 2024-04-06](https://www.facebook.com/reel/1120775405906015/)
- **TikTok:** searches for "pirogoff tallinn" and "pirogoff.ee" found no brand account. The handles found ("pirogoff", "_pirogoff", "pirogoff3", etc.) have 0 videos, and none links to pirogoff.ee. — [TikTok search via Apify clockworks/tiktok-scraper](https://www.tiktok.com/search/user?q=pirogoff%20tallinn)
- **Name clash on Instagram:** a search for "pirogoff" returns unrelated bakeries with much bigger followings: @pirogoff_almaty (8,464), @pirogoff_ast (5,801; closed), @pirogoff_semey (4,004), @pirogoff.kzn (2,271), @pirogoff1.podolsk (1,509). No separate Russian-language Tallinn account appeared. — [IG @pirogoff_almaty](https://www.instagram.com/pirogoff_almaty/); [IG @pirogoff_semey](https://www.instagram.com/pirogoff_semey/); [IG @pirogoff.kzn](https://www.instagram.com/pirogoff.kzn/)
- Google Maps' website-contact enrichment found only the Facebook and Instagram links for Pirogoff, with no TikTok or YouTube. The site footer likewise links only to Facebook and Instagram. — [Google Maps: Pirogoff](https://www.google.com/maps/search/?api=1&query=Pirogoff&query_place_id=ChIJbfwVagDtkkYRCBclwcLspeg); [pirogoff.ee/order](https://pirogoff.ee/order/)

### Inferences
- The engagement rates (7–15%) are **not a health signal**. They divide likes from 2021–2023 by today's small follower count, and nothing has been published in nearly three years. In practice Instagram is a dormant asset.
- Engagement was **bought through giveaways**. Without them the account averaged about 14 likes and almost no comments, so the giveaways did not build a lasting audience (183 followers after 43 posts).
- Content was mainly product shots with long recipe-style descriptions plus store addresses and opening hours. It used almost no hashtags, no people, no behind-the-scenes and no short video. Captions switched between Estonian, Russian and English with no consistent rule.
- The personal (non-business) account type, the empty display name and the bio that says nothing about Tallinn or ordering all reduce discoverability. So does the crowded "pirogoff" name space on Instagram.
- Facebook carries the reviews, the ads and what little posting remains. Its address is still Ülemiste, a shop the current website no longer lists (see section 3), which suggests nobody is managing the profile data.

### Gaps
- The exact first-post date is unknown. Only 30 of 43 posts were scraped, per the brief's cap; the earliest scraped is 2021-11-25.
- Story activity, highlight contents, tagged/UGC photos, reach and impressions are not observable without the account owner's access.
- VK, Telegram, Odnoklassniki and YouTube were not checked directly, because the search quota was used up and no actor was run. None are linked from the website or Facebook.
- Facebook post counts from before 2023 were not fully retrieved (9 of 15 records reviewed).

---

## 2. Website pirogoff.ee: e-commerce, UX, speed, SEO, trust signals, legal; Google rankings

### Takeaway
pirogoff.ee is a working **WordPress/WooCommerce** shop with an Estonian and a Russian version, and no English version. It sells 31 whole pies at €19–33, with dough choice, date/time-slot delivery and bank-link payment. Product data is unusually rich (ingredients with percentages, nutrition per 100 g, allergens, shelf life). It also has many quality defects:
- a mis-set Russian canonical
- missing or wrong meta descriptions
- copy-paste errors
- a hidden PHP debug dump on every listing
- legal and allergen documents kept on Google Docs, with no privacy policy found
- a stale delivery fee in the search snippet

It ranks **#1** for "pirukad Tallinn" and "пироги Таллинн". It does **not** appear for "pirukate tellimine Tallinn", "pirukad kohaletoimetamine Tallinn", "заказать пироги Таллинн" or "pies Tallinn", or even for its own brand name "Pirogoff".

### Cited Findings
**Platform and tracking**
- The stack is WordPress with WooCommerce (high confidence) on the **Storefront** theme, served by nginx with PHP 8.4.25. Translation uses the WPML plugin. Google Tag Manager is placed by a GTM plugin, and **Google Analytics and the Meta (Facebook) Pixel** were detected. — [pirogoff.ee](https://pirogoff.ee/) (Apify website-content-crawler response headers and HTML; Apify tech-stack detector)

**Languages and structure**
- The site has an **Estonian** default and **Russian** at /ru/ (WPML flag switcher). **No English** version exists. The menu: Kõik pirukad / Soolased / Magusad / Kohaletoimetamine / Meist / Русский, plus product search and a cart widget. — [pirogoff.ee/order](https://pirogoff.ee/order/); [pirogoff.ee/ru](https://pirogoff.ee/ru/)
- The ET homepage lists **20 savoury and 11 sweet pies**. Each is a whole pie of about **0.9–1 kg** (22–24 cm round or 38×15 cm). Each comes in a choice of **yeast dough (pärmitaigen) or shortcrust (muretaigen)**, set up as WooCommerce variations with SKUs such as SALTY_024_PC_EST. — [pirogoff.ee](https://pirogoff.ee/)
- Prices range from **€19** (apple pie) to **€33** (beef, salmon-spinach, beef-paprika); most pies cost €25–29. Examples: Karjuse pirukas (Shepherd's pie) €27, Kana-puravik €30, Veiseliha-kartuli €31, Porgandipirukas €21, Kapsa-munapirukas €21. — [pirogoff.ee](https://pirogoff.ee/)
- New products are still being added: product photos uploaded in 2026-03 (pumpkin-ricotta), 2026-04 (apple-ricotta) and 2026-06 (Shepherd's pie). — [pirogoff.ee](https://pirogoff.ee/)

**Ordering, delivery and payment**
- Delivery terms (current page): the customer chooses date, time window and address. Delivery within Tallinn costs **€6.00**, and is free on orders **over €50**. Delivery outside Tallinn is "by agreement". **Payment listed: bank payment (pangamakse) at checkout only.** — [pirogoff.ee/kohaletoimetamine](https://pirogoff.ee/kohaletoimetamine/)
- In 2021–22 the terms were €5 delivery, free over €30/€40, payable by bank link or by **cash/card on receipt**. — [IG post CXyFbcutnng](https://www.instagram.com/p/CXyFbcutnng/); [IG post Ce3pvVmtue6](https://www.instagram.com/p/Ce3pvVmtue6/)
- Checkout redirects to /order/, which is titled **"Otsukorv"** (a typo for "Ostukorv", cart). /ostukorv/, /kassa/ and /kontakt/ return 404. — [pirogoff.ee/order](https://pirogoff.ee/order/); [pirogoff.ee/kontakt (404)](https://pirogoff.ee/kontakt/)
- A phone order line (+372 55 960 950) sits in the header. — [pirogoff.ee/order](https://pirogoff.ee/order/)

**Trust signals and content quality**
- Each product lists **weight, size, ingredients with % of key fillings, nutrition per 100 g, allergens and shelf life** ("24h at room temperature"). An allergen table is linked separately. — [pirogoff.ee](https://pirogoff.ee/); [Allergen sheet (Google Sheets)](https://docs.google.com/spreadsheets/d/1tC-hmmTl5LcGCORWC26s-AdB57JSnIhm/edit)
- Errors found in the product content:
  - **"Allergeenid: vesi"** (water listed as an allergen) on the Shepherd's and pork-cabbage pies.
  - The green onion-egg pie description is copied from the carrot pie ("Vürtsidega pruunistatud porgandi…").
  - The raspberry-white chocolate pie's URL slug contains Russian "копировать-копировать" ("copy-copy") and its image alt text reads "Maasika - ricotta".
  - The dough attribute on Estonian product pages is labelled in Russian ("Тесто").

  — [pirogoff.ee/product/rohelise-sibula-munapirukas](https://pirogoff.ee/product/rohelise-sibula-munapirukas/); [pirogoff.ee](https://pirogoff.ee/)
- No customer reviews, ratings or testimonials appear on the site, and the WooCommerce review tab is not present. — [pirogoff.ee/product/karjuse-pirukas-lihaga-shepherds-pie](https://pirogoff.ee/product/karjuse-pirukas-lihaga-shepherds-pie/)
- Every product card in listings is followed by a hidden `<pre style="display:none">` block containing a raw PHP `print_r` dump of variation data. The homepage HTML contains **229** such "Array(" blocks; its extracted text is about 163,000 characters. — [pirogoff.ee](https://pirogoff.ee/)
- The footer shows **OÜ Pirogoff.ee, registry code 14638232, VAT EE102147298**, info@pirogoff.ee, three shops (Haabersti Rimi hyper, Tiskre Prisma, Sõpruse Rimi) with opening hours, and links to Facebook and Instagram. — [pirogoff.ee/order](https://pirogoff.ee/order/)

**Legal pages**
- The e-shop terms ("E-poe lepingutingimused") are a link to a **Google Docs** file, and the allergen list is a Google Sheets file. No on-site terms page exists. — [E-shop terms (Google Docs)](https://docs.google.com/document/d/1ELkBJGPQwLXhFVhqbn0kWnEZmmADmaeC/edit)
- No privacy policy link appears in the header or footer, and /privaatsuspoliitika/ and /muugitingimused/ return 404. — [pirogoff.ee/privaatsuspoliitika (404)](https://pirogoff.ee/privaatsuspoliitika/)

**Page speed (PageSpeed Insights lab test, mobile, 2026-10-01 09:11 UTC)**
- Scores: **Performance 88, Accessibility 93, Best Practices 87, SEO 93**. Metrics: FCP 1.6 s, **LCP 3.5 s**, TBT 234 ms, CLS 0.02, Speed Index 2.8 s. — [PageSpeed Insights: pirogoff.ee](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fpirogoff.ee%2F)
- Flagged issues: "Reduce unused JavaScript", est. savings **484 KiB**; render-blocking resources (est. 214 ms); links without discernible names; and "Document does not have a meta description". The meta-description flag conflicts with the crawler, which found one on the homepage (see SEO below). — [PageSpeed Insights: pirogoff.ee](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fpirogoff.ee%2F)

**SEO basics**
- Titles follow "<page> ⋆ Pirogoff": ET homepage "Pagarikoda Tallinnas ⋆ Pirogoff", RU homepage "Пекарня в Таллинне ⋆ Pirogoff", delivery page "Pirukate tellimine Tallinnas ⋆ Pirogoff". — [pirogoff.ee](https://pirogoff.ee/); [pirogoff.ee/ru](https://pirogoff.ee/ru/)
- Meta descriptions exist on the home, category and delivery pages, but are **missing on all crawled Russian product pages and most Estonian ones**. Three Estonian product pages (green onion-egg, ricotta-porcini, potato-mushroom) carry the chicken-porcini description by mistake. — [pirogoff.ee/product/rohelise-sibula-munapirukas](https://pirogoff.ee/product/rohelise-sibula-munapirukas/)
- The delivery page's meta description and Google snippet still say "Kohaletoimetamine Tallinna piires – **5,00 €**", while the page body says **6,00 €**. — [pirogoff.ee/kohaletoimetamine](https://pirogoff.ee/kohaletoimetamine/); [Google: site:pirogoff.ee](http://www.google.ee/search?q=site%3Apirogoff.ee&hl=et)
- **The canonical tags are mis-set.** The RU homepage (/ru/) canonicalises to https://pirogoff.ee/ and the RU category pages to their ET equivalents (e.g. /ru/сладкие-пироги/ → /magusad-pirukad/). RU product pages are self-canonical. — [pirogoff.ee/ru](https://pirogoff.ee/ru/)
- In Google's index, the ET "Pood" page shows a Russian snippet ("Капуста c яйцами…"). Product snippets do not match their pages: the carrot pie shows pear-gorgonzola text and the apple pie shows pumpkin text. — [Google: site:pirogoff.ee](http://www.google.ee/search?q=site%3Apirogoff.ee&hl=et)
- Structured data includes a Yoast-style graph (WebPage, WebSite with SearchAction, Organization with logo, BreadcrumbList) and WooCommerce Product/Offer with price. **No LocalBusiness/Bakery schema** with addresses or opening hours was observed. — [pirogoff.ee](https://pirogoff.ee/)

**Google rankings (google.ee, desktop, top ~10 organic results, 2026-10-01)**

| Query | pirogoff.ee position | Who ranks instead (top results) |
|---|---|---|
| pirukad Tallinn | **#1** | narvakohvik.ee #2, nikolay.ee #3, grenka.ee, bakery.ee, maryapagarid.ee, Pirukapunkt FB |
| пироги Таллинн | **#1 (/ru/)** | FB group thread recommending "Николай", sjucakehouse.ee, Tripadvisor Nikolay, nikolay.ee, @osseetia_pirukad, ahjupala.ee, grenka.ee |
| pirukate tellimine Tallinn | **not in top 9** (only the IG profile at #2) | cafelyon.ee #1, Wolt Kringel, Nikolay, Sju Cake House FB/TikTok |
| pirukad kohaletoimetamine Tallinn | **not in top 11** | Paid ad: Pelm Deli. Organic: Sju Cake House IG, Gulliver Café, Nikolay FB |
| заказать пироги Таллинн | **not in top 11** | kolobok.ee #1, MomBakery TikTok/FB, Nikolay (Tripadvisor, seti.ee) |
| pies Tallinn | **site not in top 9**; the Wolt page "Pirogoff Mustakivi" is #6 | Tripadvisor (Town Hall, III Draakon), Wolt Pirukapunkt, Nikolay TikTok |
| osetiini pirukas | n/a (only 1 irrelevant result; no demand or content) | — |
| осетинские пироги Таллинн | **not present** | Yandex "Осетинские пироги" Narva mnt 90, Osseetia Pirukad FB, Lõunapäike IG |
| kook tellimine Tallinn | **not present** | ristikheinakohvik.ee, pihlaka.ee, lido.ee, cafelyon.ee, pagaripoisid.ee |
| Pirogoff (brand) | **official site not in top 8** | visitharku.com listing, CV Keskus job ad (Aug 2026), Ülemiste FB post (4 years old), Digibaas, Restaurant Guru (0 reviews), a JAMA article on surgeon N. I. Pirogoff, the IG reel, overit.ee |

Sources: [pirukad Tallinn](http://www.google.ee/search?q=pirukad+Tallinn&hl=et); [пироги Таллинн](http://www.google.ee/search?q=%D0%BF%D0%B8%D1%80%D0%BE%D0%B3%D0%B8+%D0%A2%D0%B0%D0%BB%D0%BB%D0%B8%D0%BD%D0%BD); [pirukate tellimine Tallinn](http://www.google.ee/search?q=pirukate+tellimine+Tallinn&hl=et); [pirukad kohaletoimetamine Tallinn](http://www.google.ee/search?q=pirukad+kohaletoimetamine+Tallinn&hl=et); [заказать пироги Таллинн](http://www.google.ee/search?q=%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C+%D0%BF%D0%B8%D1%80%D0%BE%D0%B3%D0%B8+%D0%A2%D0%B0%D0%BB%D0%BB%D0%B8%D0%BD%D0%BD); [pies Tallinn](http://www.google.ee/search?q=pies+Tallinn); [osetiini pirukas](http://www.google.ee/search?q=osetiini+pirukas); [осетинские пироги Таллинн](http://www.google.ee/search?q=%D0%BE%D1%81%D0%B5%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B5+%D0%BF%D0%B8%D1%80%D0%BE%D0%B3%D0%B8+%D0%A2%D0%B0%D0%BB%D0%BB%D0%B8%D0%BD%D0%BD); [kook tellimine Tallinn](http://www.google.ee/search?q=kook+tellimine+Tallinn&hl=et); [Pirogoff](http://www.google.ee/search?q=Pirogoff&hl=et)

### Inferences
- **The e-commerce basics are in place**: cart, variations, time-slot delivery, bank-link checkout and rich product data. Competitors such as Nikolay and Kolobok rank on content and reputation, not on better shop technology. The gap is execution: SEO hygiene, trust content, conversion copy and an English version.
- The **Russian canonical mistake** probably holds back the Russian category pages, even though /ru/ still ranks #1 for the broad "пироги Таллинн". Russian speakers are the clearest core audience (see section 4), so this is an easy fix with high value.
- It ranks for broad head terms but **misses every "order/delivery" intent query** in both languages. Those are the transactional queries the delivery page should win; it currently loses to Nikolay, Kolobok, Café Lyon and Sju.
- Brand-name search is weak: the site is not in the top 8 for "Pirogoff", the name collides with the 19th-century surgeon Pirogoff, and there is no Google Business Profile with reviews. The brand cannot take its own search results page.
- A lab LCP of 3.5 s and 484 KiB of unused JavaScript are fixable, and the hidden debug dumps add page weight. Overall speed is "acceptable, not good".
- Hosting legal and allergen documents on Google Docs and having no on-site privacy policy hurts trust and is a GDPR/e-commerce compliance risk. This is a legal judgement for counsel; it was not verified.

### Gaps
- Checkout could not be tested end to end. The exact payment providers (bank links, cards, Apple/Google Pay), minimum order, lead time / same-day cut-off, pickup-in-store option and cookie banner were not verified.
- PageSpeed is a single lab run. Real-user (CrUX) data was not available, and the desktop test was not run.
- Rankings come from a single, unpersonalised, non-geolocated desktop snapshot. Local-pack/Map results were not captured, and Google Ads impression share is unknowable.
- Photography quality could not be judged visually, because image CDNs were blocked. File names suggest a mix of 2021 shots and 2026 professional shots (e.g. "_MG_4244-scaled.jpg").

---

## 3. Brand identity, positioning and coherence across channels (including local listings and marketplaces)

### Takeaway
"Pirogoff" positions itself as a **handmade, generously filled whole-pie bakery** ("pagarikoda") for gatherings and family tables. The website copy reaches for "exotic and premium", and the range mixes Russian/Estonian classics with European fusion fillings. It is **not Ossetian**. The identity is incoherent across channels:
- taglines in three languages ("In Pie We Trust" EN, "Käsitsi ja armastusega tehtud pirukad!" ET, Russian-led reviews)
- a different list of shops on every channel
- an outdated Facebook address
- a Google Maps listing with no reviews at a shop the website does not list
- four Wolt venues with no rating, and no Bolt Food presence at all

### Cited Findings
- **Name and legal entity**: the trading name is "Pirogoff" and the legal name "OÜ Pirogoff.ee" (registry code 14638232), registered in Harku vald, Ilmandu küla. EMTAK sector: bread and bakery products. — [pirogoff.ee/order](https://pirogoff.ee/order/); [Digibaas: OÜ Pirogoff.ee](https://www.digibaas.ee/et/personlegal/14638232-O%C3%9C-Pirogoff.ee)
- **Value proposition, in its own words**:
  - The homepage says the bakery can produce "a wide selection of handmade savoury, sweet and **ethnic** pies". It says customers want pies "with a **claim to exoticness and premium-ness**".
  - It lists three principles: "only ideal ingredients", "no skimping on filling", "equally tasty every day".
  - It mentions "veganipirukad", but no vegan category exists in the menu.

  — [pirogoff.ee](https://pirogoff.ee/)
- The "Meist" (About) page frames the brand around celebrations, family dinners, birthdays, weddings, picnics and gifts. It uses a "the good housewife is also a businesswoman with no time" narrative and "Rule no. 1 – don't skimp on the filling". — [pirogoff.ee/meist](https://pirogoff.ee/meist/)
- **Taglines differ by channel**:
  - IG bio: "In Pie We Trust" (English).
  - FB and Wolt: "Käsitsi ja armastusega tehtud pirukad!" / "Handmade pies made with love!"
  - Website title: "Pagarikoda Tallinnas" / "Пекарня в Таллинне".

  — [Instagram @pirogoff_tln](https://www.instagram.com/pirogoff_tln/); [Facebook Pirogoff.ee](https://www.facebook.com/Pirogoff.ee); [Wolt: Pirogoff Mustakivi (Google snippet)](https://wolt.com/en/est/tallinn/venue/pirogoff-mustakivi)
- **Product mix**: Russian/Eastern-European classics (cabbage-egg, pork-cabbage, beef, poppy-seed, green onion-egg, salmon described as "our variation on the classic Russian fish pie"). European/fusion items (pear-gorgonzola, Shepherd's pie, chicken-pesto-cherry tomato, ricotta-porcini, tomato-mozzarella). Sweet fruit and ricotta pies. **No Ossetian pies** on the menu. — [pirogoff.ee](https://pirogoff.ee/)
- **Visual identity cues (text only)**:
  - The logo file is "cropped-logo-s.png" (500×311 px, alt "Pirogoff"), on WooCommerce's stock **Storefront** theme.
  - Product photos are a mix of 2021–22 uploads with Russian file names (e.g. "курица-с-белыми-грибами-Песочный-вид-1.jpg") and 2026 professional-camera uploads ("_MG_4244-scaled.jpg").

  — [pirogoff.ee/order](https://pirogoff.ee/order/); [pirogoff.ee](https://pirogoff.ee/)
- **Shop network as stated on each channel**:
  - IG 2022: Ülemiste Keskus, Haabersti Rimi hyper, Tiskre Prisma, Järve Keskus.
  - IG Feb 2023: Solaris pop-up.
  - FB Apr 2024: Ülemiste, Järve, Haabersti, Tiskre.
  - FB Jan 2025: Haabersti Rimi hyper, Kristiine keskus, Järve keskus, Solaris keskus, Tiskre Prisma.
  - Website footer, Oct 2026: Haabersti Rimi hyper, Tiskre Prisma, Sõpruse Rimi.

  — [IG post CfzMF5NNybJ](https://www.instagram.com/p/CfzMF5NNybJ/); [IG post CpAqT_6ttjE](https://www.instagram.com/p/CpAqT_6ttjE/); [FB post 2024-04-06](https://www.facebook.com/Pirogoff.ee/posts/pfbid02er6SM7SAyRCahQ7vEtrzQENq7A8gutBwyfuKQBHx9YJhkZq7vVYLqNQ5VAJn3SWWl); [FB post 2025-01-25](https://www.facebook.com/Pirogoff.ee/posts/pfbid02UrWwEnhKxQAYrd9mBmfXgBCnTDiYRnf2AGJT5MDrKMxjEoYSuq5KwmUewaWFapmdl); [pirogoff.ee/order](https://pirogoff.ee/order/)
- **Google Maps**: only **one** "Pirogoff" listing was found. It is at **Mustakivi tee 17 (inside Prisma Lasnamäe)**, category Bakery, with **no rating, 0 reviews and 2 photos**. Searches for "Pirogoff Haabersti Rimi" / "Pirogoff Tiskre Prisma" returned the host hypermarkets instead, so no separate Pirogoff pins were found there. — [Google Maps: Pirogoff](https://www.google.com/maps/search/?api=1&query=Pirogoff&query_place_id=ChIJbfwVagDtkkYRCBclwcLspeg); [Google Maps: Haabersti Rimi Hyper](https://www.google.com/maps/search/?api=1&query=Haabersti%20Rimi%20Hyper&query_place_id=ChIJBxcXOjmUkkYRIU7Ac4kHwlk)
- Restaurant Guru (RU) shows "Pirogoff, Mustakivi tee 17" with "Нет отзывов" (no reviews), updated 21 June 2026. — [Restaurant Guru: Pirogoff](https://ru.restaurantguru.com/Pirogoff-Tallinn)
- **Wolt**: four Pirogoff venues were found: **Sõpruse Rimi** (Sõpruse pst 174), **Haabersti** (Haabersti 1), **Mustakivi** (Mustakivi tee 17) and **Tiskre** (Liiva tee 61; *offline* at scrape time). All four have price level 2 and **no rating score shown**. Earlier-indexed Wolt pages "Pirogoff Solaris" and "Pirogoff Kristiine" did not appear in the 2026-10-01 scrape. — [Wolt: Pirogoff Mustakivi](https://wolt.com/en/est/tallinn/venue/pirogoff-mustakivi); [Wolt: Pirogoff Solaris (search-indexed page)](https://wolt.com/en/est/tallinn/venue/pirogoff-solaris)
- **Bolt Food**: no Pirogoff venue was returned for "Pirogoff" or "pirukad" in Tallinn. — [Bolt Food Tallinn (via Apify teodor_banea/bolt-food scraper)](https://food.bolt.eu/en-US/)
- A competitor, Pagaripoisid, operates in the **same building (Mustakivi tee 17)**. On Wolt it scores 9.6, and on Bolt ("Tähesaju") 4.81 from 2,291 ratings. — [Wolt: Pagaripoisid Mustakivi](https://wolt.com/en/est/tallinn/venue/pagaripoisid-mustakivi)
- Pirogoff posted a sales-clerk ("Müüja") job ad in Tallinn in August 2026. — [CV Keskus: Müüja, OÜ Pirogoff.ee](https://www.cvkeskus.ee/muuja-tallinnas-ou-pirogoffee-1049869)

### Inferences
- The positioning is coherent in substance (handmade whole pies for occasions, generous filling) but **inconsistent in expression**. The English pun tagline, Estonian site copy, Russian-led customer base and English Facebook posts in 2024–25 speak to different audiences. The "premium/exotic" claim on the site is undercut by the stock theme, typos, debug code and inconsistent data.
- The "-off" Russified name signals a Russian-style home-baking heritage, which suits the actual Russian-speaking customer base. It also creates clashes with Kazakh/Russian "Pirogoff" bakeries and the surgeon, and it may feel "not for me" to Estonian speakers. Any rebrand decision needs consumer testing.
- The shop network seems to change often (kiosks in Ülemiste, Järve, Solaris, Kristiine and Lasnamäe have come and gone), and listings have not kept up. Name/address/phone data is wrong on Facebook (Ülemiste), Google (only Lasnamäe, no reviews) and Instagram (wrong phone). That likely costs walk-in and "near me" discovery.
- Missing ratings on Wolt and absence from Bolt Food mean Pirogoff gets no marketplace social proof. Competitors have thousands of ratings there (section 5).

### Gaps
- Logo design, colour palette, typography and **packaging** could not be assessed visually, because image hosts were blocked. A manual look at the IG grid, website and in-store packaging is needed.
- The current shop list (which kiosks are actually open in Oct 2026) conflicts across sources and should be confirmed with management.
- Wolt rating counts were not returned by the scraper (the volume field came back as 0 for every venue), so Wolt comparisons rely on the 0–10 score only.

---

## 4. Customer sentiment (reviews and comments)

### Takeaway
The little public feedback that exists is **uniformly positive**: 13 of 13 Facebook reviews recommend Pirogoff. It is **mostly in Russian** (11 of 13). Customers praise the dough, generous filling, homemade "like grandma's" taste, the wide choice, beautiful presentation, on-time and still-warm delivery, and friendly staff. The weakness is **volume**: 13 reviews in five years, no Google reviews and no Wolt rating.

### Cited Findings
- Facebook reviews: **13 reviews, 100% recommend**, dated Aug 2021 to Aug 2026. **11 are in Russian and 2 in Estonian.** — [Facebook Pirogoff.ee reviews](https://www.facebook.com/Pirogoff.ee/reviews)
- Themes, with dated examples:
  - Generous filling and good dough: "начинки много, тесто тоже понравилось" (2026-08-26) and "Очень вкусное тесто" (2024-08-18).
  - Delivered on time and still warm: "Доставлено во время. Пироги были еще теплые" (2026-03-08, salmon and feta-tomato pies).
  - Homemade taste: "как у бабушки" (2022-10-02, cabbage-egg).
  - Choice and presentation: "большой выбор вкусов… превосходная подача" (2024-08-17).
  - Festive table: "красивые пироги, как на праздничный стол" (2022-07-01).
  - Staff: named staff member "Денис" praised for service (2022-02-06).
  - Honest flavour: Estonian review praising "täidist on väga rikkalikult ja maitse on aus" (2021-11-04).
  - Kiosk visibility: a 2021 review mentions the kiosk "у входа" (at the entrance) of Haabersti Rimi.

  — [Facebook Pirogoff.ee reviews](https://www.facebook.com/Pirogoff.ee/reviews)
- Favourite products named in reviews: cabbage-egg, carrot, salmon-spinach, lemon and feta-tomato pies. — [Facebook Pirogoff.ee reviews](https://www.facebook.com/Pirogoff.ee/reviews)
- A third-party listing describes Pirogoff as having "delicious pies with a wide variety of fillings… everything is always fresh. They're filling…". — [VisitHarku: Pirogoff, Tiskre](https://www.visitharku.com/kirjed/pirogoff.html)
- Google Maps: no rating and 0 reviews (Mustakivi listing). Restaurant Guru: 0 reviews. Wolt: no score shown on any of 4 venues. — [Google Maps: Pirogoff](https://www.google.com/maps/search/?api=1&query=Pirogoff&query_place_id=ChIJbfwVagDtkkYRCBclwcLspeg); [Restaurant Guru: Pirogoff](https://ru.restaurantguru.com/Pirogoff-Tallinn); [Wolt: Pirogoff Mustakivi](https://wolt.com/en/est/tallinn/venue/pirogoff-mustakivi)
- Instagram comments are practically absent outside giveaways: median 0 per post; 344 of the 352 comments in the sample sit on one giveaway post. — [IG post CbiL4pOtyUj](https://www.instagram.com/p/CbiL4pOtyUj/)

### Inferences
- The product appears to delight those who try it. The commercial problem is **reach and reputation capture**, not product quality. A review-generation drive (Google profiles per kiosk, Wolt ratings, inserts in delivery boxes) is the cheapest credibility lever.
- The Russian-dominant reviews confirm that the core customers are Russian-speaking Tallinn residents. The Estonian-led website and English Facebook posts are not aligned with this.

### Gaps
- No negative feedback was found, so complaint themes (price, availability, freshness, delivery failures) are unknown. Management complaint logs, Wolt ratings and order data would be needed.
- Wolt reviews and Instagram DMs are not publicly scrapeable.

---

## 5. Competitive benchmark: Tallinn pie, bakery and café brands

### Takeaway
On every public reputation metric Pirogoff is **last** in the set: Instagram followers, posting cadence, Google rating and review count, Wolt/Bolt ratings. The most direct rival is **Nikolay Bar-buffeé**, a Russian-speaking whole-pie specialist at Gonsiori 10. It has 4.7★ from 1,981 Google reviews, 4.82★ from 17,828 Bolt ratings, a 21,495-like Facebook page, active bilingual Meta ads, and ranks for most pie-ordering queries. **Sju Cake House** (reels-led, about 5 posts a week, 4.92★ on Bolt) and **Kolobok** (top result for "заказать пироги Таллинн") are the other close substitutes. Pagaripoisid (5 venues, co-located with Pirogoff Mustakivi) dominates the chain/bakery segment on the delivery apps.

### Cited Findings

**Benchmark table (all values measured 2026-10-01; "—" = not found or not applicable)**

| Brand (type) | Instagram followers / posts | IG cadence (recent sample) | Google rating (reviews) | Wolt score (0–10) | Bolt Food rating (no. ratings) | Website e-commerce |
|---|---|---|---|---|---|---|
| **Pirogoff** (whole pies, mall kiosks + delivery) | 183 / 43 | 0 posts since 2023-12-17 | Lasnamäe listing: no rating (0) | 4 venues, no score; Tiskre offline | **Not listed** | Yes: WooCommerce, ET/RU, bank-link pay, €6 delivery (free >€50) |
| **Nikolay Bar-buffeé** (Russian-style pie café, Gonsiori 10) | No IG found (FB page 21,495 likes) | — | 4.7 (1,981) | 9.2 | **4.82 (17,828)** | Yes: online pie ordering (e.g. turkey-prune 1 kg €32 / 1.5 kg €48, "В корзину") |
| **Sju Cake House** (pastry/pie studio, Tammsaare tee 137, delivery) | 767 / 390; 14 highlights | ~5 posts/week in Sept 2026; 9 of last 12 are Reels; also on TikTok | 4.8 (71) | 9.6 | **4.92 (1,911)** | Website on OpenCart (low-confidence detection); RU pies page |
| **Pagaripoisid** (bakery chain, 5+ venues) | 1,058 / 251 | ~0.7/week; like counts near 0 (likely hidden) | 4.5 (799), Vana-Lõuna | 9.6–9.8 (5 venues) | 4.74–4.92 (518–2,291 per venue) | Yes: e-shop for cakes, kringles, party snacks; Meta Pixel |
| **RØST** (artisan sourdough bakery, Rotermann) | **8,054** / 90 | Very low: 12 posts from 2022-12 to 2026-04; avg 149 likes | **4.8 (3,103)** | — (not in sample) | — | — |
| **Reval Café** (13-café chain) | 2,682 / 717 | ~1.7/week; avg 23 likes | 4.5 (1,970), Müürivahe | 9.0–9.4 | 4.58–4.78 (327–1,353) | Catering/cakes (not audited) |
| **Kalamaja Pagarikoda** (bakery café) | 1,011 / 162 | ~0.4/week; avg 7 likes | 4.7 (1,020) | — | — | — |
| **Café Lyon** (bakery-café chain) | 1,158 / 778 | not computed | Meistri 4.4 (947); Ülemiste 3.3 (48) | — | 4.72 (2,279), Meistri | Yes: cake/pie ordering; #1 for "pirukate tellimine Tallinn" |
| **Lille Pagariäri** (craft bakery café, Tehnika 35) | 480 / 64 | ~0.6/week; avg 32 likes (ER ≈ 6.8%) | 4.7 (29) | 8.4 | 4.61 (90) | Courier delivery €6 (per earlier search snippet) |
| **Kolobok** (Russian-style pastry, Mahtra 17) | not found | — | not scraped | — | 4.74 (3,862) | Pie pre-order page, 24 h lead, district fees €5–7; #1 for "заказать пироги Таллинн" |
| **Pirukapunkt** (Estonian pirukas shop, Pärnu mnt 106) | not found (FB 590+ followers) | — | 4.9 (41) | 9.8 | — | — |
| **Café Narva** (Soviet-nostalgia café, pirukad e-shop) | 2,317 / 329 | not computed | 4.3 (1,764) | — | — | Yes: pirukad e-shop; #2 for "pirukad Tallinn" |
| **Kentmanni Sõõrikukohvik** (doughnut café) | no IG found | — | 4.7 (1,271) | Sõõriku Jaam 9.0 | — | — |
| **Osseetia Pirukad** (Ossetian pies, Narva mnt 90) | 360+ / 99 (SERP snippet) | — | not scraped | — | — | Previously on Bolt/Wolt (2021–22 FB post) |
| Kohvik Komeet | — | — | **Permanently closed** (4.4, 1,069) | — | — | — |

Table sources:
- Pirogoff: [Instagram](https://www.instagram.com/pirogoff_tln/); [Google Maps](https://www.google.com/maps/search/?api=1&query=Pirogoff&query_place_id=ChIJbfwVagDtkkYRCBclwcLspeg); [Wolt](https://wolt.com/en/est/tallinn/venue/pirogoff-mustakivi); [website](https://pirogoff.ee/kohaletoimetamine/)
- Nikolay: [Google Maps](https://www.google.com/maps/search/?api=1&query=Nikolay%20Bar-buffe%C3%A9); [nikolay.ee (RU order page)](https://nikolay.ee/?lang=); [Facebook Ad Library page data](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=EE&q=%D0%BF%D0%B8%D1%80%D0%BE%D0%B3%D0%B8&search_type=keyword_unordered&media_type=all)
- Sju Cake House: [Instagram](https://www.instagram.com/sjucakehouse/); [Google Maps](https://www.google.com/maps/search/?api=1&query=Sju%20Cake%20House&query_place_id=ChIJd8_7f8SVkkYREXV-XOyTclA); [TikTok](https://www.tiktok.com/@sju.cake.house/video/7656785291327393046); [RU pies page](https://sjucakehouse.ee/pies-ru)
- Pagaripoisid: [Instagram](https://www.instagram.com/pagaripoisid/); [Google Maps](https://www.google.com/maps/search/?api=1&query=Pagaripoisid%20Ltd.&query_place_id=ChIJQdK3cr2UkkYReq1EtD936vo); [website](https://www.pagaripoisid.ee/)
- RØST: [Instagram](https://www.instagram.com/rostpagar/); [Google Maps](https://www.google.com/maps/search/?api=1&query=R%C3%98ST%20Bakery&query_place_id=ChIJP73vtWCTkkYRAAmn7hNt9aM)
- Reval Café: [Instagram](https://www.instagram.com/reval_cafe/); [Google Maps](https://www.google.com/maps/search/?api=1&query=Reval%20Cafe%20M%C3%BC%C3%BCrivahe&query_place_id=ChIJgV_GCJ6UkkYR_oztJWH4FF0)
- Kalamaja Pagarikoda: [Instagram](https://www.instagram.com/kalamajapagarikoda/); [Google Maps](https://www.google.com/maps/search/?api=1&query=Kalamaja%20Bakery&query_place_id=ChIJj1TYVnqTkkYRqp9mU8r8gog)
- Café Lyon: [Instagram](https://www.instagram.com/cafelyon/); [Google Maps Ülemiste](https://www.google.com/maps/search/?api=1&query=%C3%9Clemiste%20Caf%C3%A9%20Lyon%20pagarikoda%20%26%20kohvik&query_place_id=ChIJbVhmikbrkkYRcRgsuoigclk); [cafelyon.ee](https://cafelyon.ee/kategooria/kingitused-arikingid/)
- Lille Pagariäri: [Instagram](https://www.instagram.com/lillepagar/); [Google Maps](https://www.google.com/maps/search/?api=1&query=Lille%20Pagari%C3%A4ri&query_place_id=ChIJr0w-kz2VkkYRTaFmpoxY6lw); [lillepagar.ee snacks/delivery page](http://lillepagar.ee/snkid)
- Kolobok: [kolobok.ee](https://kolobok.ee/pie-order.html)
- Pirukapunkt: [Wolt](https://wolt.com/en/est/tallinn/venue/pirukapunkt1/collections/popular)
- Café Narva: [Instagram](https://www.instagram.com/narvakohvik/); [narvakohvik.ee](https://narvakohvik.ee/catalog/pirukad)
- Sõõrikukohvik: [Google Maps](https://www.google.com/maps/search/?api=1&query=Kentmanni%20S%C3%B5%C3%B5rikukohvik&query_place_id=ChIJnemElqGUkkYR-UKxIzwiSWY)
- Osseetia Pirukad: [Instagram](https://www.instagram.com/osseetia_pirukad/)
- Bolt Food figures for all brands: [Bolt Food (via Apify scraper)](https://food.bolt.eu/en-US/)

**Engagement rates (my calculation: mean likes + comments on the latest 12 posts ÷ followers)**
- RØST 1.87%, Sju Cake House 1.24%, Reval Café 0.87%, Kalamaja Pagarikoda 0.68%, Lille Pagariäri 6.75%. Pagaripoisid is not computable (likes hidden or near 0). Pirogoff 6.9–15% on posts from 2021–23 (not current). — [IG @rostpagar](https://www.instagram.com/rostpagar/); [IG @sjucakehouse](https://www.instagram.com/sjucakehouse/); [IG @reval_cafe](https://www.instagram.com/reval_cafe/); [IG @kalamajapagarikoda](https://www.instagram.com/kalamajapagarikoda/); [IG @lillepagar](https://www.instagram.com/lillepagar/)

**Price points for whole pies**
- Pirogoff: €19–33 per 0.9–1 kg. — [pirogoff.ee](https://pirogoff.ee/)
- Nikolay: €32 per 1 kg, €48 per 1.5 kg (turkey-prune; duck-apple listed). Nikolay markets "60% filling, 40% puff-yeast dough" and sells 1.5 and 2 kg pies. — [nikolay.ee](https://nikolay.ee/?lang=); [SETI.ee (2021)](https://www.seti.ee/modules/news/article.php?storyid=121728)
- Grenka: €18 per 1 kg (cabbage) to €32 (meat/salmon). — [grenka.ee](https://www.grenka.ee/rus-pies)

**Word of mouth**
- A 2026 Russian-language Facebook advice group thread ("where to get tasty pies") recommends "Николай" on Gonsiori. — [FB group "Ищу совета (Эстония)"](https://www.facebook.com/groups/advice.search/posts/3490629967768651/)

### Inferences
- **The closest rivals for Pirogoff's customer base are Nikolay, Kolobok, Sju Cake House and Grenka**: Russian-speaking, whole-pie, ordered for occasions. All have thousands of delivery-app ratings and strong word of mouth. Nikolay sets the price and quality reference at the same price level as Pirogoff (about €32/kg) and wins on reputation, search visibility, Bolt and Wolt presence, and active ads.
- Pirogoff could differentiate on **fusion/European fillings** (pear-gorgonzola, Shepherd's pie, ricotta pies), **two dough options**, and **full nutrition and allergen disclosure**. None of the competitors reviewed communicates these.
- On Instagram, follower count is driven by a destination café (RØST 8k with almost no posting). Cadence and Reels drive local relevance (Sju at about 5 a week). A realistic first-year target for Pirogoff is the 1,000–2,500-follower band of mid-size local bakeries.
- Listing on Bolt Food and earning a Wolt score are table stakes in this category. Every direct competitor except Osseetia has a strong rating on at least one platform.

### Gaps
- Nikolay's and Kolobok's Instagram/TikTok handles were not identified (guessed handles returned "not found").
- Wolt rating counts were unavailable, and Bolt/Wolt scores are not comparable with each other (Bolt 5-point, Wolt 10-point).
- Chain ratings are shown for a single location (the first Google Maps match) unless a range is given.
- Rukis, Gourmet Coffee, Jahu (only Jahu Burgers & Bakery Volta on Wolt, 8.6; Bolt 4.68, 118 ratings), Tallinna Pagarid and Lõunapäike (Ossetian, IG 150+) were not fully profiled.

---

## 6. Paid advertising (Meta Ad Library; Google Ads observations)

### Takeaway
Pirogoff **does advertise**: Meta **catalog/Dynamic Product Ads** have run almost continuously since **March 2024**, plus a summer 2026 discount campaign. Two DPA ads were **active on 2026-10-01** (started 2026-09-26). The creative is generic (copy lifted from the delivery page) and points to a site with the conversion and trust gaps above. The organic channels that would support the ads (Instagram, reviews) are dormant. No Pirogoff Google Ads were seen. Nikolay is the only direct pie competitor seen running Meta ads in the snapshot.

### Cited Findings
- Ad Library search "Pirogoff", country EE, all statuses, first 15 results requested: **8 Pirogoff.ee ads** returned.
  - **DPA format, started 2024-03-25.** Several versions ran until 2026-03-03, 2026-07-28 and 2026-07-29. They ran on Facebook, Instagram, Audience Network and Messenger. Copy: "Soovite kodupirukaid, kuid pole aega või soovi mütata taigna ja täidistega… Pirukate tellimine – suurepärane võimalus…". Landing pages: /kohaletoimetamine/ or a Facebook Canvas.
  - **Image ads, 2026-07-28 → 2026-08-02 and 2026-08-02 → 2026-08-30**: "Suve lõpuni –20% soodustust kõikidelt veebitellimustelt alates 100 €, sooduskood HOTSUMMER10020". Also placed on Threads.
  - **2 DPA ads active on 2026-10-01** (started 2026-09-26; Facebook + Instagram), with the same delivery copy.

  — [Meta Ad Library: "Pirogoff", EE](https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=EE&q=Pirogoff&search_type=keyword_unordered&media_type=all)
- The Facebook page itself shows "This Page is currently running ads". — [Facebook Pirogoff.ee](https://www.facebook.com/Pirogoff.ee)
- The same summer promo was posted organically on Facebook on 2026-07-24 (ET + EN), with 3 likes and 2 shares. — [FB post 2026-07-24](https://www.facebook.com/Pirogoff.ee/posts/pfbid036tFZmbuiU22QXrwuSEtXXyqybuTdDLUxYEHqwNmwbHXzhksZvvFJ42T9s2fLGF2ml)
- Competitors' active ads in EE on 2026-10-01:
  - **Bar-Buffeé Nikolay** (21,495 page likes) ran a bilingual ET/RU multi-image ad from 2026-09-24 promoting a new dessert, with copy about pies for birthdays and family celebrations. Found via the keyword "пироги".
  - Keyword "pirukad" returned only non-competitors (Minurehvid, Pärnu Keskus, Tartu Rahvaülikool, Kodukiri, Barbora).
  - Keyword "Pagaripoisid" returned 0 active ads.

  — [Meta Ad Library: "пироги", EE, active](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=EE&q=%D0%BF%D0%B8%D1%80%D0%BE%D0%B3%D0%B8&search_type=keyword_unordered&media_type=all); [Meta Ad Library: "pirukad", EE, active](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=EE&q=pirukad&search_type=keyword_unordered&media_type=all); [Meta Ad Library: "Pagaripoisid", EE, active](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=EE&q=Pagaripoisid&search_type=keyword_unordered&media_type=all)
- The Meta Pixel and Google Analytics are installed on pirogoff.ee, which makes catalog retargeting possible. Pagaripoisid also runs a Meta Pixel; Nikolay and Sju show only Google Analytics. — [pirogoff.ee](https://pirogoff.ee/); [pagaripoisid.ee](https://www.pagaripoisid.ee/)
- Google Ads: across the 7 Estonian-language queries scraped with ad capture, the only paid result was **Pelm Deli** on "pirukad kohaletoimetamine Tallinn". No Pirogoff search ads were seen. — [Google: pirukad kohaletoimetamine Tallinn](http://www.google.ee/search?q=pirukad+kohaletoimetamine+Tallinn&hl=et)

### Inferences
- Running DPA retargeting for about 2.5 years with copy taken from the delivery page, a weak social profile and no reviews is likely inefficient. People who click through land on a site with typos, stale fees and no testimonials. The ad budget is probably the only "active marketing", and it is not backed by organic proof.
- The 20% off ≥€100 summer code targets large (event) orders. That fits the whole-pie occasion positioning, but there is no visible organic or influencer support for it.
- **Google Ads gap**: transactional queries such as "pirukad kohaletoimetamine Tallinn" and "заказать пироги Таллинн" have little paid competition (only Pelm Deli was seen). That points to an affordable opportunity, which needs Keyword Planner validation.

### Gaps
- Spend, reach and impressions are not shown for non-political Estonian ads in the Ad Library, so budget and ROAS are unknown. EU reach breakdowns were not pulled (`isDetailsPerAd` was not enabled).
- The total historical Pirogoff ad count may exceed 8, because the request was capped at 15 results per query.
- Google Ads history (Ads Transparency Center) was not checked. Russian-language queries were scraped without paid-ad capture.
