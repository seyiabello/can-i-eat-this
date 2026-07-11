const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type SafetyStatus = "safe" | "unsafe" | "unverified";

export type MenuItem = {
  item: string;
  allergen_notes_raw: string;
  confirmed_allergens: string[];
  ambiguous_flag: boolean;
  ambiguous_reason: string | null;
  price: string | null;
};

export type AllergenResponse = {
  status: SafetyStatus;
  item: string | null;
  explanation: string;
  matched_allergens: string[];
};

async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export function fetchMenu(): Promise<MenuItem[]> {
  return apiGet("/menu");
}

export function askQuestion(question: string): Promise<AllergenResponse> {
  return apiPost("/ask", { question });
}

export function checkAllergen(item: string, allergen: string): Promise<AllergenResponse> {
  return apiPost("/check", { item, allergen });
}

export function scanAllergen(allergen: string): Promise<AllergenResponse[]> {
  return apiGet(`/allergen-check?allergen=${encodeURIComponent(allergen)}`);
}
