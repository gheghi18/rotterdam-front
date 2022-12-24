<script>
  import TREES from "./trees.json";
  import FIELDS from "./fields.js";
  import Tree from "./Tree.svelte";
  import TextTree from "./TextTree.svelte";

  export let userFields = [];

  const trees = TREES.trees;

  let treeIndex = 0;
  let interval;

  clearInterval(interval);

  interval = setInterval(() => {
    treeIndex = treeIndex + 1;
    if (treeIndex >= trees.length - 1) {
      clearInterval(interval);
    }
  }, 100);
</script>

<section>

  <!--
    {#each Array(treeIndex + 1) as _, index (index)}
      <div class="text-tree">
        <h3>Tree {index + 1}</h3>
        <TextTree data={trees[index]} {userFields} />
      </div>

      <div class="tree">
        <Tree data={trees[index]} {index} {userFields} />
      </div>
    {/each}
  -->


  <div class="text-trees">
    {#each Array(treeIndex + 1) as _, index (index)}
      <div class="text-tree">
        <h3>Tree {index + 1}</h3>
        <TextTree data={trees[index]} {userFields} />
      </div>
    {/each}
  </div>

  <div class="trees">
    {#each Array(treeIndex + 1) as _, index (index)}
      <div class="tree">
        <Tree data={trees[index]} {index} {userFields} />
      </div>
    {/each}
  </div>
</section>

<style>
  section {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
</style>
