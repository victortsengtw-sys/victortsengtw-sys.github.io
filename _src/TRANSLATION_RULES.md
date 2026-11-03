# Translating 「讀懂非洲」 articles into English and French (victseng.com)

For each slug you are given, read /home/claude/b3/notes/<slug>/zh.md and write:
- /home/claude/b3/notes/<slug>/en.md  (skip if it already exists)
- /home/claude/b3/notes/<slug>/fr.md

Rules
1. Faithful translation of the Chinese article: same facts, same numbers, same structure (same ## sections, tables, lists). Do not add new facts, opinions or personal anecdotes. Do not drop sourced facts.
2. Natural, polished prose for an international professional reader — not word-for-word. English: British spelling is fine; write "Côte d'Ivoire" (never "Ivory Coast"). French: proper typography (espace insécable before : ; ! ?, « guillemets »), "la Côte d'Ivoire".
3. The first-mention hint becomes — EN: "Côte d'Ivoire (in West Africa, French-speaking, the world's largest cocoa producer)"; FR: "la Côte d'Ivoire (Afrique de l'Ouest, premier producteur mondial de cacao)".
4. Chinese-reader framing ("台灣", "亞洲讀者") becomes "Asian readers/companies" in EN and "lecteurs/entreprises asiatiques" in FR. Closing section heading — EN: "## One line for Asian readers" (or "...for Asian companies/teams" matching the Chinese); FR: "## En un mot, pour les lecteurs asiatiques" (or entreprises/équipes).
5. Keep French and local terms in their original form; in the French version do not add Chinese.
6. Keep the reference line and every link URL unchanged; translate only link labels where they are Chinese. EN: "*References: ...*"; FR: "*Sources : ...*".
7. Front matter: translate title and description (description 120–160 characters, keyword-rich), keep date, translate tags (3–5), and set pillar EXACTLY to:
   - 非洲藝術與品味 → EN "African Art & Taste" / FR "Art africain et goût"
   - 生活風格 → EN "Lifestyle" / FR "Art de vivre"
   - 跨文化溝通 → EN "Cross-cultural Communication" / FR "Communication interculturelle"
   - 非洲商業與市場 → EN "African Business & Markets" / FR "Business et marchés africains"
8. Format:
---
title: ...
description: ...
date: <same as zh>
pillar: <exact value above>
tags: a, b, c
---

<body>

Do not touch zh.md or any other file. When done reply with the slugs completed and anything you were unsure about (one line each).
