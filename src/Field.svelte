<script>
  import { userFields } from "./stores.js";
  export let show = true;

  export let feature_dutch_underscore,
    feature_dutch,
    feature_english_auto_translate,
    description_english,
    feature_importance,
    notes,
    understand,
    default_value,
    sum,
    category,
    index;

  let val = default_value;

  function updateStore() {
    $userFields[index] = parseFloat(val);
  }
</script>

<p class="field">
  <label for={feature_dutch_underscore}>{feature_english_auto_translate}</label>
  <input
    name={feature_dutch_underscore}
    type="number"
    step="0.01"
    bind:value={val}
    on:change={updateStore}
  />
  <small>{description_english}</small>
</p>

<style>
  .field {
    margin: 0;
  }
</style>
