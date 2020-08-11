import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Map from "./components/Map";
import UploadFile from "./components/UploadFile";

function App() {
  return (
    <div className='App'>
      <UploadFile />
      <Map />
    </div>
  );
}

export default App;
