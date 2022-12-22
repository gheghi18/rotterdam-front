<script>
  import TREES from "./trees.json";
  import Tree from "./Tree.svelte";
  import { userFields } from "./stores.js";


  const keys = TREES.keys;
  const trees = TREES.trees;

  // let allTrees = [trees[1], trees[2], trees[3]];
  let allTrees = trees;
  // allTrees = [];

</script>

<section>
  {#each allTrees as t, i}
    <!-- <p>Tree number {i}</p> -->
    <Tree data={t} index={i} userFields={$userFields}/>
  {/each}
</section>

<style>
  section {
    display: grid;
    grid-template-columns: 1fr;
  }
</style>
