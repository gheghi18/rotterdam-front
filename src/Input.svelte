<script>
  import FIELDS from "./fields.js";
  import Field from "./Field.svelte";
  import { userFields } from "./stores.js";

  const dev = false;
  const URL = dev ? "http://localhost:8080/" : "https://rotterdam-model.fly.dev/";
  const AUTH = dev ? "" : "uApjBhZ4w6h2aFQp3nx9gQFfwnJGxqoaEGeeof7H";

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

  onSort();
  onResetValues();

  function onRandomize() {
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
  }

  function onResetValues() {
    userFields.set(FIELDS.map((f) => f.default_value));
  }

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
</script>

<form on:submit|preventDefault={onSubmit}>
  <div class="fields">
    {#each sortedFields as field, index}
      <Field {...field} />
    {/each}
  </div>
  <div class="form-options">
    <select bind:value={sort} on:change={onSort}>
      <option value="alphabetical">Sort alphabetically</option>
      <option value="importance">Sort by importance</option>
    </select>

    <select bind:value={show} on:change={onFilter}>
      <option value="all">Show all fields</option>
      <option value="important">Show most important fields</option>
    </select>
  </div>
</form>

<style>
  .fields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 30px;
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
