"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  askQuestion,
  checkAllergen,
  fetchMenu,
  type AllergenResponse,
  type MenuItem,
} from "@/lib/api";
import { ALLERGENS, label } from "@/lib/allergens";

const STATUS_STYLES: Record<
  AllergenResponse["status"],
  { border: string; bg: string; ink: string; heading: string }
> = {
  safe: {
    border: "border-success-border",
    bg: "bg-success-surface",
    ink: "text-success-ink",
    heading: "Safe",
  },
  unsafe: {
    border: "border-danger-border",
    bg: "bg-danger-surface",
    ink: "text-danger-ink",
    heading: "Unsafe",
  },
  unverified: {
    border: "border-warning-border",
    bg: "bg-warning-surface",
    ink: "text-warning-ink",
    heading: "Can't confirm - ask staff",
  },
};

export default function Home() {
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [menuError, setMenuError] = useState<string | null>(null);
  const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null);
  const [result, setResult] = useState<AllergenResponse | null>(null);
  const [asking, setAsking] = useState(false);
  const [askError, setAskError] = useState<string | null>(null);
  const [freeText, setFreeText] = useState("");

  useEffect(() => {
    fetchMenu()
      .then(setMenu)
      .catch(() => setMenuError("Couldn't load the menu. Is the backend running?"));
  }, []);

  async function runCheck(item: string, allergen: string) {
    setAsking(true);
    setAskError(null);
    setResult(null);
    try {
      const res = await checkAllergen(item, allergen);
      setResult(res);
    } catch {
      setAskError("Couldn't reach the allergen check. Try again.");
    } finally {
      setAsking(false);
    }
  }

  async function runQuery(question: string) {
    setAsking(true);
    setAskError(null);
    setResult(null);
    try {
      const res = await askQuestion(question);
      setResult(res);
    } catch {
      setAskError("Couldn't reach the allergen check. Try again.");
    } finally {
      setAsking(false);
    }
  }

  function reset() {
    setSelectedItem(null);
    setResult(null);
    setAskError(null);
    setFreeText("");
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col gap-6 px-5 py-8">
      <header>
        <h1 className="text-2xl font-semibold text-ink">Can I eat this?</h1>
        <p className="mt-1 text-sm text-ink-muted">
          Pick a dish, then pick an allergen. Two taps, no typing.
        </p>
      </header>

      {menuError && (
        <p className="rounded-lg border border-danger-border bg-danger-surface px-4 py-3 text-sm text-danger-ink">
          {menuError}
        </p>
      )}

      {!selectedItem && (
        <section className="flex flex-col gap-3">
          <h2 className="text-sm font-medium text-ink-secondary">1. Select a dish</h2>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {menu.map((item) => (
              <button
                key={item.item}
                onClick={() => setSelectedItem(item)}
                className="flex flex-col items-start rounded-lg border border-border bg-surface px-4 py-3 text-left transition hover:border-border-strong hover:bg-surface-raised"
              >
                <span className="text-sm font-medium text-ink">{item.item}</span>
                {item.price && (
                  <span className="mt-1 text-xs text-ink-faint">{item.price}</span>
                )}
              </button>
            ))}
          </div>
        </section>
      )}

      {!selectedItem && (
        <section className="flex flex-col gap-3 border-t border-border pt-6">
          <div>
            <h2 className="text-sm font-medium text-ink-secondary">
              Counter view
            </h2>
            <p className="mt-1 text-xs text-ink-faint">
              What a QR code on the counter/menu would open - the whole menu
              scanned for one allergen, no dish-picking needed.
            </p>
          </div>
          <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
            {ALLERGENS.map((allergen) => (
              <Link
                key={allergen}
                href={`/allergen/${allergen}`}
                className="rounded-lg border border-border bg-surface px-3 py-2 text-center text-xs font-medium text-ink-secondary transition hover:border-signal hover:bg-surface-raised hover:text-ink"
              >
                {label(allergen)}
              </Link>
            ))}
          </div>
        </section>
      )}

      {selectedItem && !result && !asking && (
        <section className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-ink-secondary">
              2. Any allergen in <span className="text-ink">{selectedItem.item}</span>?
            </h2>
            <button onClick={reset} className="text-xs text-ink-faint underline">
              back
            </button>
          </div>
          <div className="grid grid-cols-3 gap-2 sm:grid-cols-4">
            {ALLERGENS.map((allergen) => (
              <button
                key={allergen}
                onClick={() => runCheck(selectedItem.item, allergen)}
                className="rounded-lg border border-border bg-surface px-3 py-3 text-sm font-medium text-ink transition hover:border-signal hover:bg-surface-raised"
              >
                {label(allergen)}
              </button>
            ))}
          </div>

          <div className="mt-2 flex flex-col gap-2">
            <label className="text-xs text-ink-faint" htmlFor="free-text">
              Or ask something specific
            </label>
            <div className="flex gap-2">
              <input
                id="free-text"
                value={freeText}
                onChange={(e) => setFreeText(e.target.value)}
                placeholder="e.g. is this okay for a shellfish allergy?"
                className="flex-1 rounded-lg border border-border bg-surface px-3 py-2 text-sm text-ink placeholder:text-ink-faint focus:border-signal focus:outline-none"
              />
              <button
                disabled={!freeText.trim()}
                onClick={() => runQuery(`${freeText.trim()} (about ${selectedItem.item})`)}
                className="rounded-lg bg-signal px-4 py-2 text-sm font-medium text-white transition hover:bg-signal-deep disabled:opacity-40"
              >
                Ask
              </button>
            </div>
          </div>
        </section>
      )}

      {asking && (
        <section className="flex flex-col gap-2">
          <div className="skeleton h-20 w-full rounded-xl" />
          <p className="text-xs text-ink-faint">Checking...</p>
        </section>
      )}

      {askError && (
        <p className="rounded-lg border border-danger-border bg-danger-surface px-4 py-3 text-sm text-danger-ink">
          {askError}
        </p>
      )}

      {result && !asking && (
        <section className="flex flex-col gap-4">
          <div
            className={`fade-rise-in rounded-xl border ${STATUS_STYLES[result.status].border} ${STATUS_STYLES[result.status].bg} px-5 py-6`}
          >
            <p className={`text-lg font-semibold ${STATUS_STYLES[result.status].ink}`}>
              {STATUS_STYLES[result.status].heading}
            </p>
            {result.item && (
              <p className="mt-1 text-sm text-ink-secondary">{result.item}</p>
            )}
            <p className="mt-3 text-sm text-ink-secondary">{result.explanation}</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setResult(null)}
              className="flex-1 rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium text-ink hover:border-border-strong"
            >
              Ask about another allergen
            </button>
            <button
              onClick={reset}
              className="flex-1 rounded-lg bg-signal px-4 py-2 text-sm font-medium text-white hover:bg-signal-deep"
            >
              New dish
            </button>
          </div>
        </section>
      )}
    </main>
  );
}
