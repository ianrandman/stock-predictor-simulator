import React from 'react';
import './App.css';
import Routes from '../routes';
import {BrowserRouter} from "react-router-dom";

function App() {
  return (
    <div className="application">
      <h1>I am a header</h1>
      <hr/>

      <Routes/>
    </div>
  );
}

export default App;
