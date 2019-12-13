import React, { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';
import { HashRouter as Router, Route, Switch, Redirect } from "react-router-dom";




import { Provider as AlertProvider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";

import Header from './layout/Header';
import Clth_Dashboard from './cloths/Dashboard';
import Ord_Dashboard from './orders/Dashboard';
import Alerts from "./layout/Alerts";
import Del_Dashboard from './delivery/Dashboard';

import { Provider } from 'react-redux';
import store from '../store';
import {Orders} from './orders/Orders';
import { Cloths } from './cloths/Cloths';


const alertOptions = {
  timeout: 3000,
  position: 'top center'
}

export default function  App (){
    return (
      <Provider store={store}>
      <AlertProvider template={AlertTemplate} {...alertOptions}>
        <Router>
        <Fragment>
          <Header />
          <div className="container">
          <Switch>
            <Route exact path="/" component={Ord_Dashboard} />
            <Route path="/cloths/" component={Clth_Dashboard} />
            <Route path="/orders/" component={Ord_Dashboard} />
            <Route path="/delivery/" component={Del_Dashboard} />
          </Switch>
          </div>
        </Fragment>
        </Router>
      </AlertProvider>
      </Provider>
    );
}



ReactDOM.render(<App />, document.getElementById('app'));
