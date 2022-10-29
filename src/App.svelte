<script>
  import FIELDS from "./features.json";
  import Field from "./Field.svelte";
  import { userFields } from "./stores.js";

  function onSort() {
    sortedFields = sortedFields.sort(sorters[sort]);
  }

  function onFilter() {
    if (show == "all") {
      sortedFields = FIELDS.sort(sorters[sort]);
    } else {
      sortedFields = FIELDS.filter((f) => f.feature_importance > 10);
      onSort();
    }
  }

  function onRandomize() {
    userFields.set(FIELDS.map((f) => parseInt(Math.random() * 100)));
  }

  function onResetValues() {
    userFields.set(FIELDS.map((f) => f.default_value));
  }

  async function onSubmit(e) {
    loading = true;
    let data = { auth: AUTH, d: [$userFields] };
    let response = await fetch(URL, {
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

  const URL = "https://rotterdam-model.fly.dev/";
  // const URL = "http://localhost:8080/";
  const AUTH = "uApjBhZ4w6h2aFQp3nx9gQFfwnJGxqoaEGeeof7H";

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
  let show = "all";


  let sortedFields = FIELDS.sort(sorters[sort]);
  onResetValues();
</script>

<main>
  <form on:submit|preventDefault={onSubmit}>
    <header>
      <div class="check-score">
        <h1>
          Score:
          {#if loading}
            ...
          {:else}
            {score}
          {/if}
        </h1>
        <button type="submit">Check Score</button>
      </div>

      <select bind:value={sort} on:change={onSort}>
        <option value="alphabetical">Sort alphabetically</option>
        <option value="importance">Sort by importance</option>
      </select>

      <select bind:value={show} on:change={onFilter}>
        <option value="all">Show all fields</option>
        <option value="important">Show most important fields</option>
      </select>

      <p>
        <button on:click|preventDefault={onResetValues}>Reset to average values</button>
      </p>
      <p>
        <button on:click|preventDefault={onRandomize}>Randomize values</button>
      </p>
    </header>

    <div class="fields">
      {#each sortedFields as field, index}
        <Field {...field} />
      {/each}
    </div>
  </form>
</main>

<style>
  header {
    position: fixed;
    width: 250px;
  }

  header select {
    width: 100%;
    margin-bottom: 10px;
  }

  .check-score {
    margin-bottom: 30px;
  }

  .fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 30px;
    margin-left: 300px;
    /* display: flex; */
    /* flex-wrap: wrap; */
  }

  h1 {
    font-size: 3em;
    font-weight: normal;
    margin-top: 0;
  }

  button {
    font-size: 2em;
    padding: 20px;
    width: 100%;
  }
</style>
