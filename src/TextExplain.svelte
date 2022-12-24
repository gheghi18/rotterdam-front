<script>
  import TREES from "./trees.json";
  import FIELDS from "./fields.js";

  export let userFields = [];

  let sentences = [];

  const featureKey = {};

  for (const f of FIELDS) {
    featureKey[f.index] = f;
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

  // const _sentences = [];
  //
  // for (const key in reasons) {
  //   let s = `Because ${featureKey[key]} is `;
  //   let clauses = reasons[key]
  //     .map((r) => {
  //       const [comp, split] = r.split("::");
  //       if (comp == "true" || comp == "false") {
  //         return comp;
  //       } else {
  //         return `${comp} than ${split}`;
  //       }
  //     })
  //     .join(" and ");
  //   s += clauses;
  //   _sentences.push(s);
  // }
  // sentences = _sentences;

  let explainations = [];

  for (const key in reasons) {
    const item = {};
    item.name = featureKey[key].feature_english_auto_translate;
    item.clauses = reasons[key].map((r) => {
      const [comp, split] = r.split("::");
      return { comp, split };
    });
    explainations.push(item);
  }
</script>

<section>
  {#each explainations as e}
    <p>
      Because {e.name} is
      {#each e.clauses as c, i}
        {#if c.comp == "true" || c.comp == "false"}{c.comp}{:else}{c.comp} than {c.split}{/if}{#if i < e.clauses.length - 1}
          , and{" "}
        {:else}.{/if}
      {/each}
    </p>
  {/each}
</section>

<style>
  p {
  }
</style>
