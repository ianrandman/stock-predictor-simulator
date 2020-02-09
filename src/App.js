import React from 'react';
import Routes from './routes';
import {BrowserRouter} from "react-router-dom";
import 'typeface-roboto';

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
