<script>
  import TREES from "./trees.json";
  import FIELDS from "./fields.js";
  import { userFields } from "./stores.js";

  // export let userFields = [];
  export let data;
  export let traceFeature;

  const featureKey = {};

  for (const f of FIELDS) {
    featureKey[f.index] = f;
  }

  const keys = TREES.keys;
  const trees = TREES.trees;

  let score = null;
  let index = 0;
  let explanations = [];

  while (score === null) {
    const [t_id, var_id, split, left, right] = data[index];
    if (var_id == -1) {
      score = split;
      break;
    }
    const inp = $userFields[var_id];
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

  // let clauses = explanations.map(e => {
  //   if (e.type == "boolean") return `${e.name.toLowerCase()} is ${e.comparison}`;
  //   else return `${e.name.toLowerCase()} is ${e.comparison} than ${e.split}`;
  // }).join(", and ");
  //
  // let sentence = `Because ${clauses}, the score is ${score}.`;
</script>

<p>
  Because
  {#each explanations as e, index}
    <span class="name" on:click={traceFeature(e.var_id)}>{e.name.toLowerCase()}</span> is
    {#if e.type == "boolean"}
      <span class="comp">{e.comparison}</span>{#if index < explanations.length - 1}, and {" "}{:else},{/if}
    {:else}
      <span class="comp">{e.comparison} than {e.split}</span>{#if index < explanations.length - 1}, and {" "}{:else},{/if}
    {/if}
  {/each}
  the score is <span class="score">{score}</span>.
</p>

<!--  -->
<!-- 
{#each explanations as e}
  <p>
    Because <span class="name">{e.name.toLowerCase()}</span> is
    {#if e.type == "boolean"}
      <span class="comp">{e.comparison}</span>.
    {:else}
      <span class="comp">{e.comparison} than {e.split}</span>.
    {/if}
  </p>
{/each}
<p>Score is <span class="score">{score}</span>.</p>
 -->
<style>
  p {
    line-height: 1.5;
  }
  .name {
    /* text-decoration: underline; */
    border-bottom: 1px solid blue;
    /* background-color: yellow; */
    cursor: pointer;
  }
  .comp {
    border-bottom: 1px solid red;
    /* background-color: lightblue; */
  }
  .score {
    border-bottom: 1px solid orange;
    /* background-color: orange; */
  }
</style>
