<script>
  import {userFields} from "./stores.js";
  export let en;
  export let nl;
  export let show=true;
  export let weight;
  export let def;
  export let index;

  let val=def;

  function updateStore() {
    $userFields[index] = val;
  }

</script>

<p class="field">
  <label for={nl}>{nl}</label>
  <input name={nl} type="number" bind:value={val} on:change={updateStore} />
</p>

<style>
  .field {
    margin: 0;
  }
</style>
