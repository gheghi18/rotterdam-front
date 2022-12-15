<script>
  import TREES from "./trees.json";
  import FIELDS from "./features.json";

  export let userFields = [];

  let sentences = [];

  const featureKey = {};

  for (const f of FIELDS) {
    featureKey[f.index] = f.feature_english_auto_translate;
  }

  const keys = TREES.keys;
  const trees = TREES.trees;
  let reasons = {};

  for (let tree of trees) {
    let score = null;
    let index = 0;
    while (score === null) {
      const [t_id, var_id, split, left, right] = tree[index];
      if (var_id == -1) {
        score = split;
        break;
      }
      const inp = userFields[var_id];
      let comparison;
      if (split == 0.5) {
        comparison = inp < split ? "false" : "true";
      } else {
        comparison = inp < split ? "less" : "more";
      }
      // const comparison = inp < split ? "less" : "more";
      const out = comparison + "::" + split;

      if (!reasons[var_id]) reasons[var_id] = [];
      if (!reasons[var_id].includes(out)) reasons[var_id].push(out);

      // reason = (name, inp, split, comparison, out)
      // reasons["reasons"].append(reason)

      if (inp < split) {
        index = left;
      } else {
        index = right;
      }
    }
  }
  const _sentences = [];
  for (const key in reasons) {
    let s = `Because ${featureKey[key]} is `;
    let clauses = reasons[key]
      .map((r) => {
        const [comp, split] = r.split("::");
        if (comp == "true" || comp == "false") {
          return comp;
        } else {
          return `${comp} than ${split}`;
        }
      })
      .join(" and ");
    s += clauses;
    _sentences.push(s);
  }
  sentences = _sentences;
</script>

{#each sentences as sentence}
  <p>{sentence}</p>
{/each}
