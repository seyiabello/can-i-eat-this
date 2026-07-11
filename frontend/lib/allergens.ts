export const ALLERGENS = [
  "gluten",
  "milk",
  "eggs",
  "fish",
  "crustaceans",
  "molluscs",
  "mustard",
  "nuts",
  "peanuts",
  "sesame",
  "soya",
  "sulphites",
  "celery",
  "lupin",
];

export function label(word: string) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}
