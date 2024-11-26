import "bootstrap/dist/css/bootstrap.min.css";
import "./cssc/core.css";

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";

import Main from "./core.jsx";
import { data } from "./features/data.jsx";

createRoot(document.getElementById("root")).render(
  <Provider store={data}>
    <StrictMode>
      <Main />
    </StrictMode>
  </Provider>
);
