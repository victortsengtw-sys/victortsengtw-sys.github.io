# Finding openly licensed images for 「讀懂非洲」 articles (victseng.com)

Goal: for each slug you are given, find ONE relevant image that is free to reuse, or decide "none".
Read /home/claude/b3/notes/<slug>/zh.md (title + first section) to understand the topic.

ALLOWED licences only (verify on the file page itself):
- Public domain / CC0 (incl. The Met "Open Access" / CC0, Smithsonian Open Access CC0, Rijksmuseum CC0, US government works)
- CC BY (any version) or CC BY-SA (any version) — attribution required, record author exactly as shown.
NOT allowed: anything "all rights reserved", "fair use", non-commercial (NC), no-derivatives (ND), unknown licence, Flickr images without a clear CC BY/BY-SA, stock sites, news photos, Pinterest, Google Images.

Where to look: Wikimedia Commons (commons.wikimedia.org) first; The Met collection (metmuseum.org, Open Access objects show "Public Domain"); Smithsonian Open Access. Use WebSearch to find candidate file pages, then WebFetch the file page to confirm licence, author and exact file name.

Content rules
- Prefer places, landscapes, architecture, objects in museum collections, textiles, food, markets seen from a distance.
- NO public figures or celebrities; NO close-up portraits of identifiable private people; no children in focus; nothing violent or degrading; no images whose page flags them as sacred/restricted.
- For abstract topics (tax, labour law, procurement, email etiquette, numbers…) choose a neutral relevant image only if clearly fitting (e.g. Abidjan Plateau skyline for business topics, a document/handshake is NOT needed) — otherwise "none". It is fine to return "none" for up to a third of slugs.
- Do not reuse the same image for two slugs in your batch.

Output: write ONE JSON file /home/claude/b3/data/img/<batch-name>.json containing an object keyed by slug:
{
  "<slug>": {
    "file": "<exact Commons file name without 'File:' prefix, e.g. Basilique Notre-Dame de la Paix Yamoussoukro.jpg>",   // for Commons
    "src": "<direct image URL>",          // for Commons use: https://commons.wikimedia.org/wiki/Special:FilePath/<URL-encoded file name>?width=1200 ; for The Met use the 'primaryImage' web-large URL from the object page or API
    "page": "<file/object page URL>",
    "author": "<author / creator as credited, or museum name for CC0>",
    "license": "<e.g. CC BY-SA 4.0 | CC BY 2.0 | Public domain | CC0>",
    "license_url": "<licence deed URL, or empty for public domain>",
    "alt": {"zh": "<繁體中文 alt>", "en": "<English alt>", "fr": "<texte alternatif français>"},
    "caption": {"zh": "<短圖說>", "en": "<short caption>", "fr": "<courte légende>"}
  },
  "<slug-without-image>": null
}
Captions describe what is shown only (no new facts beyond what the file page states). Do not touch any other files.
Reply with a one-line summary per slug.
