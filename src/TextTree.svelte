<script>
  import TREES from "./trees.json";
  import FIELDS from "./fields.js";
  import Tree from "./Tree.svelte";

  export let userFields = [];
  export let data;

  let explanations = [];

  const featureKey = {};

  for (const f of FIELDS) {
    featureKey[f.index] = f;
  }

  const keys = TREES.keys;
  const trees = TREES.trees;

  let score = null;
  let index = 0;

  while (score === null) {
    const [t_id, var_id, split, left, right] = data[index];
    if (var_id == -1) {
      score = split;
      break;
    }
    const inp = userFields[var_id];
    const type = featureKey[var_id].type;
    let comparison;
    if (type == "boolean") {
      comparison = inp < split ? "false" : "true";
    } else {
      comparison = inp < split ? "less" : "more";
    }
    // const comparison = inp < split ? "less" : "more";
    const name = featureKey[var_id].feature_english_auto_translate;
    explanations.push({ var_id, name, type, inp, split, comparison });

    if (inp < split) {
      index = left;
    } else {
      index = right;
    }
  }
</script>

{#each explanations as e}
  <p>
    Because {e.name} is
    {#if e.type == "boolean"}
      {e.comparison}.
    {:else}
      {e.comparison} than {e.split}.
    {/if}
  </p>

{/each}
<p>Score is {score}.</p>
