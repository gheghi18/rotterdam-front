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
    type,
    feature_english,
    index;
</script>

<div class="field" id={"field-" + index}>
  <div class="input-holder">
    {#if type == "boolean"}
      <select name={feature_dutch_underscore} bind:value={$userFields[index]}>
        <option value={0.0}>False</option>
        <option value={1.0}>True</option>
      </select>
    {:else}
      <input
        name={feature_dutch_underscore}
        type="number"
        step={type == "float" ? 0.01 : 1}
        bind:value={$userFields[index]}
      />
    {/if}
  </div>
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
    font-size: 0.8em;
    color: #777;
  }

  input,
  select {
    font-size: 20px;
    font-family: Times, sans-serif;
    border: 1px solid #000;
    /* width: 5em; */
    /* width: 100%; */
    /* display: block; */
    width: 110px;
    padding: 10px;
    text-align: center;
    background-color: #fff;
  }
  select {
  }
  .input-holder {
    margin-right: 20px;
    width: 110px;
  }
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    opacity: 1;
  }
  /* .field { */
  /*   margin: 0; */
  /* } */
</style>
