# Blueprint Homepage Visual Implementation Plan (Revised)

**Goal**: Create a cohesive homepage that feels like browsing an engineer's project journal — with blueprint covers (Hero/Footer) and warm, lived-in notebook pages throughout.

**Unified Visual Language**:
- **Blueprint** (Hero, Programmes, Footer) — The "covers" and title pages
- **Engineer's Notebook** (everything else) — Warm, lived-in journal pages

---

## Design Principles

### What Makes Field Notes Work (and we should extend)
1. **Graph paper backgrounds** — varying opacity (0.02-0.08)
2. **Taped/pinned elements** — photos feel placed by hand
3. **Paper texture and layering** — subtle shadows, overlapping elements
4. **Margin annotations** — handwritten-style notes in Courier
5. **Slight rotations** — 0.5-2deg for organic, placed-by-hand feel
6. **Warm cream tones** — not stark white

### What to Avoid
- Multiple distinct document types (patent sheets, org charts, bill of materials)
- Cold, sterile specification styling
- Over-engineered complexity

---

## Section Overview (Simplified)

| Section | Treatment | Work Needed |
|---------|-----------|-------------|
| Navigation | Light polish | Minimal — add monospace labels |
| Hero | Blueprint | Complete |
| Programmes | Blueprint | Complete |
| Alumni Initiatives | Notebook page | Add taped card frames |
| Alumni Outcomes | Notebook pages | Unify with taped photos/clippings style |
| Field Notes | Notebook | Complete (reference implementation) |
| Mentors | Notebook page | Style as pinned headshots |
| Supporters | Notebook page | Style as stamps/stickers |
| Apply | Complete | Already works |
| Footer | Blueprint | Add blue background to bookend |

---

## 1. Navigation Bar

### Approach: Light Polish Only
Keep current structure. Add subtle technical typography.

### Changes
- Monospace font for nav links (Courier New)
- Slightly increase letter-spacing (0.05em)
- Keep everything else as-is

### Files
- `src/components/sections/Header.astro` (minor CSS tweaks)

---

## 2. Alumni-Led Initiatives

### Approach: Notebook Page with Taped Project Cards
Cards feel like project photos taped into a journal with handwritten labels.

### Visual Elements
- **Graph paper background** — 20px grid at ~0.04 opacity
- **Tape corners** — Semi-transparent yellow tape on card corners
- **Slight rotations** — Each card rotated 0.3-0.8deg alternating
- **Handwritten figure labels** — "PROJECT 01", "PROJECT 02" in margin

### CSS Pattern (extend from Field Notes)
```css
.initiatives-page {
    position: relative;
    background: var(--color-cream-50);
}
.initiatives-page::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        linear-gradient(#e8e8e8 1px, transparent 1px),
        linear-gradient(90deg, #e8e8e8 1px, transparent 1px);
    background-size: 20px 20px;
    opacity: 0.04;
}
.initiative-card {
    transform: rotate(-0.5deg);
    position: relative;
}
.initiative-card .tape {
    /* Reuse tape styling from FieldNotesSection */
}
```

### Files
- `src/pages/index.astro` (wrap section, add tape elements to cards)

---

## 3. Alumni Outcomes (All Three Subsections)

### Approach: Unified Notebook Clippings
All three feel like pages of the same journal — photos and notes taped in.

### Visual Elements (same across all three)
- **Graph paper background** — consistent with initiatives
- **Taped photos** — all images have tape corners
- **Margin annotations** — company names, dates as handwritten notes
- **Paper layering** — subtle shadows suggesting overlapping clippings
- **Red margin line** — optional, like notebook pages

### No Distinct Metaphors
Instead of "patent drawings" vs "lab notebook" vs "ID badges":
- Companies Founded = Taped photos with caption annotations
- Research & Academia = Taped photos with caption annotations
- Industry = Taped photos with caption annotations

They're all just different pages of the same journal.

### CSS Pattern
```css
.outcome-photo {
    transform: rotate(1deg);
    box-shadow: 2px 3px 8px rgba(0,0,0,0.1);
}
.outcome-photo .tape-tl,
.outcome-photo .tape-tr {
    /* Tape corner styling */
}
.outcome-caption {
    font-family: 'Courier New', monospace;
    font-size: 0.75rem;
    transform: rotate(-1deg);
    margin-top: 8px;
}
```

### Files
- `src/pages/index.astro` (inline styling for outcome sections)

---

## 4. Mentors Section

### Approach: Pinned Headshots Page
Mentor photos pinned to a notebook page — like a team board in a lab.

### Visual Elements
- **Graph paper background** — consistent with other sections
- **Pinned photos** — Each headshot has a pushpin or tape effect
- **Slight rotations** — 0.3-1deg alternating
- **Handwritten names** — Monospace labels below each photo
- **Optional margin note** — "ADVISORS" written vertically in margin

### CSS Pattern
```css
.mentor-card {
    transform: rotate(0.5deg);
    background: white;
    padding: 8px;
    box-shadow: 2px 3px 8px rgba(0,0,0,0.08);
}
.mentor-card::before {
    /* Pushpin or tape effect at top */
    content: '';
    position: absolute;
    top: -4px;
    left: 50%;
    width: 12px;
    height: 12px;
    background: #c44;
    border-radius: 50%;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.3);
}
```

### Files
- `src/components/sections/MentorsSection.astro`
- `src/components/cards/MentorCard.astro`

---

## 5. Supporters Section

### Approach: Logo Stamps/Stickers
Logos feel like stamps or stickers collected in a notebook.

### Visual Elements
- **Subtle paper background** — consistent cream
- **Stamp-like presentation** — logos with slight shadow, some rotated
- **Tape/sticker effect** — optional border or paper edge
- **Simple layout** — no table structure, just organic arrangement

### CSS Pattern
```css
.supporter-logo {
    transform: rotate(-0.5deg);
    filter: grayscale(50%);
    opacity: 0.8;
    transition: all 0.2s;
}
.supporter-logo:hover {
    filter: grayscale(0%);
    opacity: 1;
    transform: rotate(0deg) scale(1.02);
}
```

### Files
- `src/components/sections/SupportersSection.astro` (light styling changes)

---

## 6. Footer

### Approach: Blueprint Bookend
Return to blueprint blue to close the document — like the back cover.

### Visual Elements
- **Blueprint blue background** (#4a7fbf)
- **Light grid overlay** — 40px at 0.1 opacity (lighter than Hero)
- **Monospace typography** — all text in Courier New
- **Keep content structure** — just restyle colors and typography

### CSS Pattern
```css
.footer-blueprint {
    background: #4a7fbf;
    color: #fff;
    position: relative;
}
.footer-blueprint::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px);
    background-size: 40px 40px;
}
.footer-blueprint a {
    color: rgba(255,255,255,0.85);
}
.footer-blueprint a:hover {
    color: #ffb100;
}
```

### Files
- `src/components/sections/Footer.astro`

---

## Implementation Sequence

### Phase 1: Quick Wins (30 min)
1. **Footer** — Add blueprint blue background + grid
2. **Nav** — Add monospace font to links

### Phase 2: Notebook Pages (1-2 hours)
3. **Alumni Initiatives** — Add graph paper bg + tape to cards
4. **Mentors** — Add pinned photo styling

### Phase 3: Polish (1 hour)
5. **Alumni Outcomes** — Unify all three with taped photo style
6. **Supporters** — Add stamp/sticker presentation

---

## Shared CSS Utilities

Add to `global.css`:

```css
/* Graph Paper Background Utility */
.graph-paper-bg {
    position: relative;
}
.graph-paper-bg::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        linear-gradient(#e8e8e8 1px, transparent 1px),
        linear-gradient(90deg, #e8e8e8 1px, transparent 1px);
    background-size: 20px 20px;
    opacity: 0.04;
    pointer-events: none;
}

/* Tape Effect Utility */
.tape {
    position: absolute;
    width: 30px;
    height: 12px;
    background: rgba(255, 230, 150, 0.75);
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.tape-tl { top: -6px; left: 10px; transform: rotate(-15deg); }
.tape-tr { top: -6px; right: 10px; transform: rotate(12deg); }

/* Pinned Element */
.pinned::before {
    content: '';
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 10px;
    height: 10px;
    background: #c44;
    border-radius: 50%;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.3);
}

/* Notebook Rotation Classes */
.rotate-cw-sm { transform: rotate(0.5deg); }
.rotate-ccw-sm { transform: rotate(-0.5deg); }
.rotate-cw-md { transform: rotate(1.2deg); }
.rotate-ccw-md { transform: rotate(-1.2deg); }
```

---

## Design Constants

| Element | Value |
|---------|-------|
| Blueprint Blue | #4a7fbf |
| Orange Accent | #ffb100 |
| Cream Background | #f5f4ef |
| Graph Paper Grid | 20px |
| Graph Paper Opacity | 0.04 |
| Technical Font | Courier New, monospace |
| Tape Color | rgba(255, 230, 150, 0.75) |
| Pushpin Red | #c44 |
| Rotation Range | 0.3deg - 1.5deg |

---

## Critical Files

- `src/pages/index.astro` — Main page sections
- `src/components/sections/Footer.astro` — Blueprint footer
- `src/components/sections/Header.astro` — Nav polish
- `src/components/sections/MentorsSection.astro` — Pinned photos
- `src/components/sections/SupportersSection.astro` — Stamps
- `src/styles/global.css` — Shared utilities
