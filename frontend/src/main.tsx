/** Entry point for the React application. */
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

/**
 * Render the App component to the DOM.
 * Uses React 18's new root API for concurrent features.
 */
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
