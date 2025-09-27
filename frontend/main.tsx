/*
 * Main entry point for the MyBrand Job Application Platform frontend
 * 
 * This file serves as the central initialization point for the React application.
 * It bootstraps the entire frontend by:
 * 1. Creating the React root element
 * 2. Rendering the main App component within React's strict mode
 * 3. Connecting to the DOM element with ID 'root'
 * 
 * The application follows a component-based architecture with:
 * - React for UI rendering
 * - React Router for navigation
 * - React Query for data fetching and caching
 * - Tailwind CSS for styling
 */

// Import core React libraries for component creation and DOM rendering
import React from "react";
import ReactDOM from "react-dom/client";

// Import the main application component that contains all routes and providers
import App from "./App";

/*
 * Create and render the React application root
 * 
 * ReactDOM.createRoot() creates a root for the React application that will be
 * rendered into the DOM element with ID 'root'. This is the modern React 18
 * approach for concurrent rendering.
 * 
 * The App component is wrapped in React.StrictMode which helps identify
 * potential problems in the application by intentionally double-invoking
 * certain functions during development.
 */
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);