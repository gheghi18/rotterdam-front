<script>
  import { onMount } from "svelte";
  import { hierarchy, tree } from "d3";
  import {lang} from "./stores.js";
  import FIELDS from "./fields.js";

  export let data;
  export let index;
  export let userFields = [];

  const featureKey = {};
  for (const f of FIELDS) {
    featureKey[f.index] = f;
  }

  // for (let uf of $userFields) {
  //   console.log(uf);
  // }

  let selected = [];

  function makeTree(_data) {
    function make(data, rownum, selected) {
      const [t_id, var_id, split, left, right] = data[rownum];
      let name;
      if (var_id >= 0) {
        name = $lang == "en" ? featureKey[var_id].feature_english_auto_translate : featureKey[var_id].feature_dutch;
      } else {
        name = split.toFixed(4);
      }
      const type = var_id >= 0 ? featureKey[var_id].type : null;
      const item = { name, selected, var_id, type, split, t_id, children: [], id: "t" + t_id };

      if (var_id != -1) {
        let leftSelected = false;
        let rightSelected = false;
        if (selected) {
          leftSelected = userFields[var_id] < split;
          rightSelected = !leftSelected;
        }
        item.children[0] = make(data, left, leftSelected);
        item.children[1] = make(data, right, rightSelected);
      }
      return item;
    }

    let tree = make(_data, 0, true);
    return tree;
  }

  let g;
  let x = 0;
  let y = 0;
  let w = 500;
  let h = 500;

  const padding = 5;

  let treeData = makeTree(data);

  const root = hierarchy(treeData);

  // const treeGen = tree().size([900, 500])
  const treeGen = tree().nodeSize([100, 150]);
  const treeX = treeGen(root);
  // treeX.each((t) => {
  //   const x = t.x;
  //   t.x = t.y;
  //   t.y = x;
  // });

  onMount(() => {
    const bbox = g.getBBox();
    x = bbox.x - padding;
    y = bbox.y - padding;
    w = bbox.width + padding * 2;
    h = bbox.height + padding * 2;
  });
</script>

<svg viewbox={[x, y, w, h]}>
  <g bind:this={g}>
    {#each treeX.links() as link}
      {#if link.target.x > link.source.x}
        <path
          id={link.source.data.id + link.target.data.id + index}
          class:selected={link.source.data.selected && link.target.data.selected}
          d={"M" + link.source.x + " " + link.source.y + " L" + link.target.x + " " + link.target.y}
        />
      {:else}
        <path
          id={link.source.data.id + link.target.data.id + index}
          class:selected={link.source.data.selected && link.target.data.selected}
          d={"M" + link.target.x + " " + link.target.y + " L" + link.source.x + " " + link.source.y}
        />
      {/if}
      <text
        class="split"
        dy="-3"
        class:selected={link.source.data.selected && link.target.data.selected}
      >
        <textPath
          startOffset="50%"
          class="split"
          href={"#" + link.source.data.id + link.target.data.id + index}
        >
          {#if link.target.x > link.source.x}
            {link.source.data.type == "boolean" ? "true" : " >= " + link.source.data.split}
          {:else}
            {link.source.data.type == "boolean" ? "false" : link.source.data.split + " > "}
          {/if}
        </textPath>
      </text>
    {/each}

    {#each treeX.descendants() as d}
      <foreignObject x={d.x - 50} y={d.y - 30} width={100} height={150}>
        <p class="label" class:selected={d.data.selected}>{d.data.name}</p>
      </foreignObject>
    {/each}
  </g>
</svg>

<style>
  path {
    stroke: #000;
    stroke-width: 1px;
  }
  .label {
    font-size: 12px;
    text-align: center;
    background-color: #fff;
    padding: 3px;
    /* border: 1px solid #999; */
    /* border-radius: 10px; */
  }
  .split {
    font-size: 11px;
    text-anchor: middle;
  }
  .label.selected {
    background-color: orange;
  }
  path.selected {
    stroke: orange;
  }
  text.selected {
    fill: orange;
  }
</style>
