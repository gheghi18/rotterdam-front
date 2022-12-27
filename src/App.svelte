<script>
  import FIELDS from "./fields.js";
  import Field from "./Field.svelte";
  import { userFields } from "./stores.js";
  // import TextExplain from "./TextExplain.svelte";
  import TextTree from "./TextTree.svelte";
  import Tree from "./Tree.svelte";
  import TREES from "./trees.json";
  import { fade } from "svelte/transition";
  import LazyLoad from "@dimfeld/svelte-lazyload";

  // const worker = new Worker(new URL("./worker.js", import.meta.url), {
  //   type: "module",
  // });

  const dev = false;
  const APIURL = dev ? "http://localhost:8080/" : "https://rotterdam-model.fly.dev/";
  const AUTH = dev ? "" : "uApjBhZ4w6h2aFQp3nx9gQFfwnJGxqoaEGeeof7H";
  const trees = TREES.trees;

  const sorters = {
    alphabetical: (a, b) =>
      a.feature_english_auto_translate
        .toLowerCase()
        .localeCompare(b.feature_english_auto_translate.toLowerCase()),
    importance: (a, b) => b.feature_importance - a.feature_importance,
  };

  const archetypes = [
    { name: "Migrant Man", main_fields: [10, 20, 30], hidden_fields: [] },
    { name: "Young Woman", main_fields: [11, 21, 31], hidden_fields: [] },
    { name: "Single Mom", main_fields: [12, 22, 33], hidden_fields: [] },
  ];

  let score = 0;
  let loading = false;
  let sort = "alphabetical";
  let show = "important";
  let explainView = "text";
  let treeIndex = 499;
  let fieldElements = [];

  let sortedFields = [...FIELDS].sort(sorters[sort]);
  onResetValues();
  onFilter();

  function onSort() {
    sortedFields = [...sortedFields].sort(sorters[sort]);
  }

  function onFilter() {
    if (show == "all") {
      sortedFields = [...FIELDS].sort(sorters[sort]);
    } else {
      sortedFields = FIELDS.filter((f) => f.feature_importance > 10);
      onSort();
    }
  }

  function toggleText() {
    showText = !showText;
  }

  function onRandomize() {
    // randomizing = true;
    // console.log(fieldElements);
    for (let f of fieldElements) {
      f.animate();
    }
    setTimeout(() => {
      userFields.set(
        FIELDS.map((f) => {
          if (f.type == "boolean") {
            return Math.random() < 0.5 ? 0.0 : 1.0;
          } else if (f.type == "float") {
            return +(Math.random() * 100).toFixed(1);
          } else {
            return parseInt(Math.random() * 100);
          }
        })
      );
    }, 300);
  }

  function onResetValues() {
    userFields.set(FIELDS.map((f) => f.default_value));
  }

  function onChangeView() {}

  async function onSubmit(e) {
    loading = true;
    let data = { auth: AUTH, d: [$userFields] };
    let response = await fetch(APIURL, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    });
    let results = await response.json();
    score = results[0]["Ja"];
    loading = false;
  }
</script>

<main>
  <section>
    <header>
      <h1>Data Input</h1>
      <p>Enter your data</p>
    </header>
    <article>
      <form on:submit|preventDefault={onSubmit}>
        <div class="fields">
          {#each sortedFields as field, index}
            <Field {...field} bind:this={fieldElements[index]} />
          {/each}
        </div>
      </form>
    </article>

    <nav class="input-options">
      <div class="input-options-section">
        <p>
          <select bind:value={show} on:change={onFilter}>
            <option value="all">Show all fields</option>
            <option value="important">Show most important fields</option>
          </select>
        </p>
        <p>
          <select bind:value={sort} on:change={onSort}>
            <option value="alphabetical">Sort alphabetically</option>
            <option value="importance">Sort by importance</option>
          </select>
        </p>
      </div>

      <div class="input-options-section">
        <p><button on:click|preventDefault={onResetValues}>Reset to average values</button></p>
        <p><button on:click|preventDefault={onRandomize}>Randomize values</button></p>
      </div>

      <button class="check-score" disabled={loading} on:click|preventDefault={onSubmit}
        >Run Model</button
      >
    </nav>
  </section>

  <section>
    <header class="output">
      <h1>Model Output</h1>
      <p>
        <select bind:value={explainView} on:change={onChangeView}
          ><option value="text">View the modelling results as text</option><option value="trees"
            >View the modelling results as trees</option
          ></select
        >
      </p>
    </header>
    <article>
      {#if score != 0 && loading === false}
        {#if explainView == "trees"}
          <div class="text-trees">
            {#key score}
              {#each Array(treeIndex + 1) as _, index (index)}
                <LazyLoad>
                  <div class="text-tree" in:fade={{ duration: 2000 }}>
                    <h3>Tree {index + 1}</h3>
                    <Tree data={trees[index]} {index} userFields={$userFields} />
                  </div>
                </LazyLoad>
              {/each}
            {/key}
          </div>
        {:else}
          <div class="text-trees">
            {#key score}
              {#each Array(treeIndex + 1) as _, index (index)}
                <div class="text-tree">
                  <h3>Tree {index + 1}</h3>
                  <TextTree data={trees[index]} />
                </div>
              {/each}
            {/key}
          </div>
        {/if}
      {:else}
        <div class="no-score">
          <div>
            {#if loading}
              <p>...loading...</p>
            {:else}
              <p>Enter some data and run the model to see results.</p>
            {/if}
          </div>
        </div>
      {/if}
    </article>
    <nav class="output">
      <p class="tip">
        The model is made up of 500 decision trees. The data is sent to each tree, which outputs a
        single score. The scores produced by each tree are then used to calculate the final
        prediction.
      </p>
      <div class="score" style="background-color: hsl({100 - score * 100}, 100%, 50%)">
        <div class="score-label">Risk Score</div>
        <div class="score-value">
          {#if loading}
            <div class="loader" />
          {:else}
            {score > 0 ? score : "?"}
          {/if}
        </div>
      </div>
    </nav>
  </section>
</main>

<style>
  main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    height: 100vh;
  }

  section {
    display: grid;
    height: 100vh;
    grid-template-rows: auto 1fr auto;
  }

  section:first-child {
    border-right: 5px solid #000;
  }

  header {
    border-bottom: 2px solid #000;
    /* box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.2); */
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  header p {
    opacity: 0.7;
  }

  h1 {
    font-size: 30px;
    font-weight: normal;
    margin: 0;
  }

  nav {
    /* box-shadow: 0px -5px 10px rgba(0, 0, 0, 0.2); */
  }

  header,
  article,
  nav {
    padding: 15px;
  }

  header {
    padding: 7px 15px;
  }

  header,
  nav {
    background-color: #fffee0;
    background-color: #eee;
  }

  header.output,
  nav.output {
    background-color: #e0fdff;
    background-color: #eee;
  }

  article {
    overflow: scroll;
    border-bottom: 2px solid #000;
  }

  .input-options {
    display: flex;
    align-items: center;
  }

  .input-options p {
    margin: 0;
  }
  .input-options p:first-child {
    margin-bottom: 10px;
  }

  .input-options button,
  select {
    width: 100%;
    background-color: #fff;
    border: 1px solid #000;
    cursor: pointer;
  }

  .input-options button {
    /* border-right-width: 4px; */
    /* border-bottom-width: 4px; */
    /* border-right-color: #666; */
    box-shadow: 3px 3px 0px #000;
  }

  .input-options button:hover {
    /* background: #000; */
    /* color: #fff; */
  }

  .input-options button:active {
    position: relative;
    top: 2px;
    left: 2px;
  }

  .input-options .check-score {
    width: auto;
    height: 100%;
    background-color: yellow;
    cursor: pointer;
    margin-left: auto;
    padding: 20px;
    font-size: 1.5em;
  }

  .input-options-section {
    margin-right: 10px;
  }

  .output {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .output .tip {
    width: 50%;
    margin: 0;
  }

  .left {
  }

  .fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    /* grid-gap: 15px; */
  }

  nav {
    /* background-color: #333; */
  }

  button {
    font-size: 1em;
  }

  .score {
    display: flex;
    border: 1px solid #000;
    /* transition: all 3s; */
    /* background-color: hsl(100, 100%, 50%); */
  }

  .score-label,
  .score-value {
    padding: 10px;
    text-align: center;
  }

  .score-label {
    border-right: 1px solid #000;
    font-size: 0.9em;
    /* color: #fff; */
  }

  .score-value {
    font-size: 30px;
    /* color: #fff; */
  }

  h3 {
    font-weight: normal;
    border-bottom: 1px solid #000;
  }

  .no-score {
    display: grid;
    place-items: center;
    height: 100%;
    font-size: 2em;
    color: #888;
    background-color: #eee;
  }
</style>
