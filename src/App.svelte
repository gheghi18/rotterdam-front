<script>
  import { FIELDS } from "./fields.js";
  import Field from "./Field.svelte";
  import { userFields } from "./stores.js";

  // const URL = "https://rotterdam-api.fly.dev/";
  const URL = "http://localhost:8080/";
  const AUTH = "uApjBhZ4w6h2aFQp3nx9gQFfwnJGxqoaEGeeof7H";

  let score=0;

  async function handleSubmit(e) {
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
  }
</script>

<main>
  <h1>{score}</h1>
  <form on:submit|preventDefault={handleSubmit}>
    <input type="submit" value="Submit" />
    {#each FIELDS as field, index}
      <Field {...field} {index} />
    {/each}
  </form>
</main>

<style>
</style>
