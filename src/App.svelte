<script>
  import FIELDS from "./features.json";
  import Field from "./Field.svelte";
  import { userFields } from "./stores.js";

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

  let score = 0;
  let loading = false;
  let sort = "alphabetical";

  let sortedFields = FIELDS.sort(sorters[sort]);

  function onSort() {
    sortedFields = sortedFields.sort(sorters[sort]);
  }

  async function onSubmit(e) {
    loading = true;
    let data = { auth: AUTH, d: [$userFields] };
    console.log(data);
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

  .check-score {
    margin-bottom: 30px;
  }

  select {
    width: 100%;
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
