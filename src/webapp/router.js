import React from 'react';
import Home from './components/Home';
import Login from './components/login';
import {Switch,Route} from 'react-router-dom'

export default class Router extends React.Component{

    render(){
        return(
            <Router>
                <Switch>
                    <Route path='/'>
                        <Home/>
                    </Route>
                    <Route path='/login'>
                        <Login/>
                    </Route>
                </Switch>
            </Router>
        )
    }
}