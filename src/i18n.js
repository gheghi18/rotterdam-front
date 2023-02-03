import translations from "./translations.json"
import { lang } from "./stores.js";

let $lang;

lang.subscribe(val => {
  $lang = val;
});

export function t(key){
  if (!translations[key]) return key;
  if (!translations[key][$lang]) return translations[key]["en"] || key;
  return translations[key][$lang]
}
