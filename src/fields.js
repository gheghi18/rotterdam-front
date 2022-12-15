import FEAUTURES from "./features.json";

const headers = FEAUTURES.headers;
const vals = FEAUTURES.values;

export default vals.map((vls) => {
  const item = {};
  for (let i = 0; i < vls.length; i++) {
    item[headers[i]] = vls[i];
  }
  return item;
});
