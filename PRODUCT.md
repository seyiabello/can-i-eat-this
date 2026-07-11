# Product

## Register

product

## Users

Two primary users, both under time pressure: a dining hall customer with a food allergy who has about thirty seconds in a queue to decide whether a dish is safe, and a server who may have started that week and doesn't know the menu yet. A secondary audience is a hiring panel watching a live demo, who need to read the screen clearly from a distance and trust it instantly.

## Product Purpose

Answer "can I eat this?" in two taps, with a result that is never a guess. Success looks like: correct classification shown immediately, the ambiguous/unverified case reads as clearly trustworthy as the safe and unsafe cases (not like an error state), and the whole thing is legible in a live demo on a laptop screen, phone screen, or projector.

## Brand Personality

Calm, direct, trustworthy. This is a life-safety tool, not a lifestyle app. It should read as clinically confident without being cold or intimidating, closer to a well-designed medical device UI than a consumer chatbot. No urgency theatrics, no playfulness. The seriousness of the subject (severe allergies) earns a plain, unambiguous interface.

## Anti-references

No generic SaaS dashboard patterns: no hero-metric cards, no gradient text, no tiny uppercase eyebrow labels, no numbered section markers used as decoration. No playful or game-like visual language given the subject matter. No dense data-table or admin-panel feel, this is a single-purpose tool used in short bursts, not a workspace someone sits in.

## Design Principles

- Color carries meaning, not decoration. The safe/unsafe/unverified system is the entire interface; every other color choice should stay out of its way.
- Never let the ambiguous state look like a lesser or broken result. It is the most important state in the product and must read as equally confident and clear as safe/unsafe.
- Optimize for a stranger glancing at a screen for two seconds, not a user settling in. Large touch targets, minimal text, no hunting.
- Legible in bad conditions: a phone screen, a laptop lid tilted at a demo, a projector. Contrast and size matter more than subtlety here.

## Accessibility & Inclusion

WCAG AA minimum. Status must never be color-only, every state needs a text label alongside its color (already true: "Safe" / "Unsafe" / "Can't confirm - ask staff"). Color choices need to hold up for red-green color blindness specifically, given the safe/unsafe pair is the whole product; distinguish by more than hue where possible (icon, position, label weight).
