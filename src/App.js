import React from 'react';
import Routes from './Routes';
import {BrowserRouter} from "react-router-dom";

class App extends React.Component {

  render() {
    return (
      <div className="application">
        <BrowserRouter>
          <Routes/>
        </BrowserRouter>
      </div>
    );
  }
}

export default App;
