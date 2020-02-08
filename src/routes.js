import React from 'react';
import { Home } from './views/Home';
import { About } from './views/About';
import { NavBar } from './components/NavBar';
import {NoMatch} from "./views/NoMatch";
import { Route, Switch, Redirect } from 'react-router-dom';

export default class Routes extends React.Component{

    render(){
        return(
          <div>
            <NavBar />
            <Switch>
              <Route exact path="/Home" component={Home} />
              <Route exact path="/">
                <Redirect to="/Home" />
              </Route>
              <Route exact path="/About" component={About} />
              <Route component={NoMatch} />
            </Switch>
          </div>
        )
    }
}