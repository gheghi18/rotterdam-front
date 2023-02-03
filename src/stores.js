import { writable } from "svelte/store";

// import FIELDS from "./fields.json";

const params = new URLSearchParams(window.location.search);

// export const userFields = writable(FIELDS.map((f) => f.default_value));
export const userFields = writable([]);
export const highlightedField = writable(-1);
export const lang = writable(params.get("lang") || "en");
