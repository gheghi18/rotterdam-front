<script>
  import TREES from "./trees.json";
  import FIELDS from "./fields.js";
  import Tree from "./Tree.svelte";

  export let userFields = [];

  let sentences = [];

  const featureKey = {};

  for (const f of FIELDS) {
    featureKey[f.index] = f;
  }

  const keys = TREES.keys;
  const trees = TREES.trees;

  function makeReasons() {
    let reasons = {};

    for (let i = 0; i <= treeIndex; i++) {
      const tree = trees[i];
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
    return explainations;
  }

  let treeIndex = 0;
  let interval;
  let explainations = makeReasons();

  clearInterval(interval);

  interval = setInterval(() => {
    treeIndex = treeIndex + 1;
    if (treeIndex >= trees.length-1) {
      clearInterval(interval);
    } else {
      explainations = makeReasons();
    }
  }, 100);
</script>

<!-- <input type="range" min="0" max="499" bind:value={treeIndex} /> -->
<section>
  <!--
  {#key treeIndex}
  <Tree data={trees[treeIndex]} index={treeIndex} userFields={userFields}/>
  {/key}
  -->
  <div class="text">
    <h3>Tree {treeIndex+1} of {trees.length}</h3>
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
  </div>
  <div class="trees">
    {#each Array(treeIndex + 1) as _, index (index)}
      <div><Tree data={trees[index]} {index} {userFields} /></div>
    {/each}
  </div>
</section>

<style>
  section {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
  .trees {
    display: flex;
    /* flex-direction: column-reverse; */
    flex-wrap: wrap-reverse;
  }
  .trees div {
    width: 25%;
  }
</style>
