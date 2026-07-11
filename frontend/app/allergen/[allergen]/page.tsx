"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { scanAllergen, type AllergenResponse } from "@/lib/api";
import { label } from "@/lib/allergens";

const STATUS_ORDER: Record<AllergenResponse["status"], number> = {
  unsafe: 0,
  unverified: 1,
  safe: 2,
};

const STATUS_STYLES: Record<
  AllergenResponse["status"],
  { border: string; bg: string; ink: string; badge: string }
> = {
  safe: {
    border: "border-success-border",
    bg: "bg-success-surface",
    ink: "text-success-ink",
    badge: "Safe",
  },
  unsafe: {
    border: "border-danger-border",
    bg: "bg-danger-surface",
    ink: "text-danger-ink",
    badge: "Unsafe",
  },
  unverified: {
    border: "border-warning-border",
    bg: "bg-warning-surface",
    ink: "text-warning-ink",
    badge: "Ask staff",
  },
};

export default function AllergenScan() {
  const params = useParams<{ allergen: string }>();
  const allergen = decodeURIComponent(params.allergen);

  const [results, setResults] = useState<AllergenResponse[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    scanAllergen(allergen)
      .then((res) => {
        const sorted = [...res].sort(
          (a, b) => STATUS_ORDER[a.status] - STATUS_ORDER[b.status]
        );
        setResults(sorted);
      })
      .catch(() => setError("Couldn't reach the menu scan. Is the backend running?"));
  }, [allergen]);

  const counts = results?.reduce(
    (acc, r) => ({ ...acc, [r.status]: (acc[r.status] ?? 0) + 1 }),
    {} as Record<string, number>
  );

  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-6 px-5 py-8">
      <header>
        <Link href="/" className="text-xs text-ink-faint underline">
          &larr; full picker
        </Link>
        <h1 className="mt-2 text-2xl font-semibold text-ink">
          {label(allergen)} - whole menu
        </h1>
        {counts && (
          <p className="mt-1 text-sm text-ink-muted">
            {counts.unsafe ?? 0} unsafe &middot; {counts.unverified ?? 0} ask staff &middot;{" "}
            {counts.safe ?? 0} safe
          </p>
        )}
      </header>

      {error && (
        <p className="rounded-lg border border-danger-border bg-danger-surface px-4 py-3 text-sm text-danger-ink">
          {error}
        </p>
      )}

      {!results && !error && (
        <div className="flex flex-col gap-2">
          <div className="skeleton h-16 w-full rounded-xl" />
          <div className="skeleton h-16 w-full rounded-xl" />
          <div className="skeleton h-16 w-full rounded-xl" />
        </div>
      )}

      {results && (
        <ul className="flex flex-col gap-2">
          {results.map((r) => {
            const styles = STATUS_STYLES[r.status];
            return (
              <li
                key={r.item}
                className={`flex items-center justify-between rounded-lg border ${styles.border} ${styles.bg} px-4 py-3`}
              >
                <div>
                  <p className="text-sm font-medium text-ink">{r.item}</p>
                  <p className="mt-0.5 text-xs text-ink-secondary">{r.explanation}</p>
                </div>
                <span className={`shrink-0 pl-3 text-xs font-semibold ${styles.ink}`}>
                  {styles.badge}
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </main>
  );
}
