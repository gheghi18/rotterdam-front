import { writable } from 'svelte/store';
import { FIELDS } from "./fields.js";

export const userFields = writable(FIELDS.map(f => f.def));
