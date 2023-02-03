import translations from "./translations.json"
import { lang } from "./stores.js";

let $lang;

lang.subscribe(val => {
  $lang = val;
});

export function t(key){
  return translations[key][$lang] || translations[key]["en"];
}
