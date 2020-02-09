import React from 'react';
import Home from './views/Home';
import About from './views/About';
import NoMatch from "./views/NoMatch";
import { Route, Switch } from 'react-router-dom';
import CandleStick from './components/CandleStick';

export default class Routes extends React.Component{
    render(){
        return(
          <div>
            <Switch>
              <Route exact path="/">
                <Home/>
              </Route>

              <Route exact path="/about">
                <About/>
              </Route>

              <Route exact path={'/test'}>
                <CandleStick/>
              </Route>

              <Route path="*">
                <NoMatch/>
              </Route>
            </Switch>
          </div>
        )
    }
}