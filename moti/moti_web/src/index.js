import 'bootstrap/dist/css/bootstrap.css';
import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import IndexPage from './IndexPage';
import './index.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import UserPage from "./UserPage";
import SnapshotPage from "./SnapshotPage";

ReactDOM.render(
   <Router>
		<Switch>
			<Route path="/:id/:snapshot" component={SnapshotPage} />
			<Route path="/:id" component={UserPage} />
			<Route path="/">
				<IndexPage />
			</Route>
		</Switch>
	</Router>,
  document.getElementById('root')
);
