---
name: Can I Eat This?
description: A two-tap allergen safety check for a dining hall counter.
colors:
  signal: "#3b82f6"
  signal-deep: "#2563eb"
  signal-bright: "#60a5fa"
  success: "#16a34a"
  success-deep: "#15803d"
  success-surface: "#052e16"
  success-border: "#166534"
  success-ink: "#86efac"
  danger-surface: "#450a0a"
  danger-border: "#991b1b"
  danger-ink: "#f87171"
  warning-surface: "#422006"
  warning-border: "#854d0e"
  warning-ink: "#facc15"
  canvas: "#030712"
  surface: "#111827"
  surface-raised: "#1f2937"
  border: "#1f2937"
  border-strong: "#374151"
  ink: "#f3f4f6"
  ink-secondary: "#d1d5db"
  ink-muted: "#9ca3af"
  ink-faint: "#6b7280"
typography:
  body:
    fontFamily: "Geist Sans, -apple-system, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Geist Sans, -apple-system, sans-serif"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "normal"
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
spacing:
  xs: "8px"
  sm: "12px"
  md: "16px"
  lg: "24px"
components:
  button-primary:
    backgroundColor: "{colors.signal}"
    textColor: "#ffffff"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  button-primary-hover:
    backgroundColor: "{colors.signal-deep}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  button-secondary-hover:
    backgroundColor: "{colors.surface-raised}"
  result-card-safe:
    backgroundColor: "{colors.success-surface}"
    textColor: "{colors.success-ink}"
    rounded: "{rounded.lg}"
    padding: "24px 20px"
  result-card-unsafe:
    backgroundColor: "{colors.danger-surface}"
    textColor: "{colors.danger-ink}"
    rounded: "{rounded.lg}"
    padding: "24px 20px"
  result-card-unverified:
    backgroundColor: "{colors.warning-surface}"
    textColor: "{colors.warning-ink}"
    rounded: "{rounded.lg}"
    padding: "24px 20px"
---

# Design System: Can I Eat This?

## 1. Overview

**Creative North Star: "The Night Shift Counter"**

Dark, quiet, low-glare, the way a well-run kitchen pass looks at 11pm: nothing shouting for attention except the one thing that needs to be seen right now. Everything in this interface is built to stay out of the way of a single message, is this dish safe or not, so almost the entire surface sits in a narrow band of near-black neutrals with no decoration, no gradients, no shadows, no accent color competing for attention. Color only ever appears to mean something. The signal blue shows up on interactive elements a user needs to find (buttons, links) and nowhere else. The safe/unsafe/unverified triad is the one place saturated color is allowed, and it always arrives with a plain-language label next to it, never alone.

This system explicitly rejects the generic SaaS dashboard look: no hero-metric cards, no gradient text, no eyebrow labels, no numbered section markers as decoration. It also rejects playful or game-like visual language. The subject is severe allergies; the interface should read like a well-designed medical device, not a consumer app.

**Key Characteristics:**
- Near-black neutral canvas, flat, no shadows
- One interactive accent (signal blue), used sparingly
- Three semantic status colors that are the actual product, never decorative
- Single typeface, no display/body pairing, because there is no marketing voice here to differentiate
- Large tap targets, short copy, built to be read in two seconds

## 2. Colors

The palette is almost entirely neutral, with color reserved for exactly two jobs: marking something interactive, and reporting a safety result.

### Primary
- **Signal Blue** (#3b82f6): the one interactive accent. Primary buttons ("Ask", "New dish"), focus rings, hover borders on pickable items. Never used to convey a safety result, that would blur the one distinction that matters most.

### Semantic (the actual product)
- **Confirmed Safe Green** (#16a34a core / #052e16 surface / #86efac ink): the safe result card and its border.
- **Confirmed Unsafe Red** (#991b1b border / #450a0a surface / #f87171 ink): the unsafe result card and its border.
- **Ask Staff Amber** (#854d0e border / #422006 surface / #facc15 ink): the unverified result card. This color must read as equally confident as the other two, never as an error or a lesser result. It is reporting a fact ("the data doesn't support a claim of safe"), not failing.

### Neutral
- **Canvas** (#030712): the page background, near-black.
- **Surface** (#111827): cards, buttons, and pickable tiles at rest.
- **Surface Raised** (#1f2937): hover state for surface elements.
- **Border / Border Strong** (#1f2937 / #374151): dividing lines, default and hover-emphasized.
- **Ink / Ink Secondary / Ink Muted / Ink Faint** (#f3f4f6 / #d1d5db / #9ca3af / #6b7280): a four-step text ramp from headings down to the least important caption on the page.

### Named Rules
**The One Meaning Rule.** Saturated color never appears for decoration. If a color isn't the signal accent or a safety status, it doesn't belong on this screen.

**The Never-Lesser Rule.** The unverified/amber state is styled with exactly the same visual weight as safe and unsafe: same card size, same font weight on the heading, same border thickness. It must never look like a fallback or an error.

## 3. Typography

**Body Font:** Geist Sans (with -apple-system, sans-serif fallback)

**Character:** One typeface for the entire interface. There is no marketing register here that needs a display face to differentiate itself from body copy, every piece of text is either a label, a question, or a safety result, so a single well-made grotesque carries all of it without needing a second voice.

### Hierarchy
- **Title** (600 weight, 24px): the page heading, "Can I eat this?"
- **Headline** (700 weight, 18px): the result card status word, "Safe" / "Unsafe" / "Can't confirm - ask staff"
- **Body** (400-500 weight, 14-16px): dish names, allergen labels, explanatory sentences
- **Label** (500 weight, 12-13px): captions, prices, helper text under inputs

### Named Rules
**The Single Voice Rule.** Do not introduce a second font family for emphasis. Weight and size carry hierarchy, not a display face.

## 4. Elevation

Flat by default, no shadows anywhere in the system. Depth is conveyed entirely through the neutral ramp: an element sits one step lighter than its background (surface on canvas, surface-raised on hover) and is edged with a 1-2px border. This matches the North Star, a kitchen counter at night has no theatrical lighting, just enough contrast to tell one surface from another.

### Named Rules
**The Flat-by-Default Rule.** No box-shadow anywhere in the system. If something needs to feel closer to the user, lighten its background one step and brighten its border, don't cast a shadow under it.

## 5. Components

### Buttons
- **Shape:** 8px radius, consistent across every button in the system
- **Primary:** signal blue background, white text, used for the one clear next action on a screen ("Ask", "New dish")
- **Secondary:** surface background, ink text, border, used for pickable tiles (dish names, allergen names) and lower-emphasis actions ("Ask about another allergen", "back")
- **Hover / Focus:** primary darkens to signal-deep; secondary brightens to surface-raised and its border shifts to signal blue

### Result Card (signature component)
- **Corner Style:** 16px radius, the largest radius in the system, marking it as the single most important element on the screen
- **Background:** the semantic surface color for its status (success/danger/warning surface)
- **Border:** 2px in the matching semantic border color
- **Internal Padding:** 24px vertical, 20px horizontal, generous enough to read at a glance
- **Content:** a bold status heading in the matching ink color, the matched item name, then a plain-language explanation sentence

### Inputs / Fields
- **Style:** surface background, 1px border, 8px radius
- **Focus:** border shifts to signal blue, no glow or shadow
- **Placeholder:** ink-faint, meets the same contrast floor as body text since placeholder legibility matters here (used for example questions)

### Pickable Tiles (dish and allergen grids)
- **Style:** surface background, border, left-aligned label, price shown as a muted caption underneath for dish tiles
- **Hover / Focus:** border brightens to border-strong or signal blue, background lifts to surface-raised
- **Selected state:** not currently distinct from hover; a picked tile simply advances the flow to the next screen rather than staying visible in a "selected" state

## 6. Do's and Don'ts

### Do:
- **Do** keep color meaning-only: signal blue for interaction, the semantic triad for results, nothing else
- **Do** give the unverified/amber state the same visual weight as safe and unsafe, per the Never-Lesser Rule
- **Do** keep every result labeled in text, never rely on color alone to communicate status
- **Do** keep the whole interface flat, per the Flat-by-Default Rule
- **Do** size tap targets for a stranger glancing at a phone or a counter screen, not a desk-bound power user

### Don't:
- **Don't** add a hero-metric card, a gradient accent, an eyebrow label, or a numbered section marker, these are the generic SaaS dashboard patterns this system explicitly rejects
- **Don't** introduce a second typeface for "personality", per the Single Voice Rule
- **Don't** add box-shadows or glassmorphism, per the Flat-by-Default Rule
- **Don't** use playful, game-like, or cutesy visual language anywhere, the subject is severe allergies
- **Don't** let the amber/unverified card read as broken, muted, or lower-priority than the other two results
