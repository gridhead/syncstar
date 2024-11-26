import compdict from "./icon.jsx";

const logodict = {
  PENDING: compdict.lesson,
  FAILURE: compdict.fiasco,
  WORKING: compdict.verify,
  SUCCESS: compdict.result,
};

const mooddict = {
  PENDING: "default",
  FAILURE: "failure",
  WORKING: "warning",
  SUCCESS: "success",
};

export { mooddict };
export { logodict };
