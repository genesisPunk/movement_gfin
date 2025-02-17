"use client";
import React from "react";
import withErrorBoundary from "../components/ErrorBoundary"; // Import the HOC
import Login from "@/components/Login";
import "@razorlabs/razorkit/style.css";

const App: React.FC = () => {
  return <Login />;
};

export default withErrorBoundary(App);
