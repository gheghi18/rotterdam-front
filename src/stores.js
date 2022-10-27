import { writable } from 'svelte/store';
import FIELDS from "./features.json";

export const userFields = writable(FIELDS.map(f => f.default_value));
