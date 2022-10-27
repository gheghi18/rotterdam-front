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

<div class="field">
  <input
    name={feature_dutch_underscore}
    type="number"
    step="0.01"
    bind:value={val}
    on:change={updateStore}
  />
  <label for={feature_dutch_underscore}>
    <div class="title">{feature_english_auto_translate}</div>
    <div class="description">{description_english}</div>
    <div class="importance">Importance: {feature_importance}%</div>
  </label>
</div>

<style>
  .field {
    /* margin: 30px 0px; */
    display: flex;
    /* max-width: 400px; */
    align-items: flex-start;
  }

  /* .field input, .field label { */
  /*   display: inline; */
  /* } */

  .field div {

  }

  .title {
    font-size: 1.3em;
    text-transform: capitalize;
  }

  .importance {
    font-size: .8em;
    color: #777;
  }

  input {
    margin-right: 20px;
    font-size: 20px;
    font-family: Times, sans-serif;
    border: 1px solid #000;
    width: 5em;
    padding: 10px;
    text-align: center;
  }
  /* .field { */
  /*   margin: 0; */
  /* } */
</style>
