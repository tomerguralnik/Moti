import React, { Component } from 'react';
import logo from './logo.png';
import './IndexPage.css';
import Textbox from "./Textbox";
import {UserLink, UsersList} from "./UsersPage";
import {Link} from "react-router-dom";

class IndexPage extends Component {
  state = {
  	id: ""
  }

  _updateId = event => {
    const value = event.target.value;
    this.setState({ id: value });
  }

  render() {
    return (
    	<div>
		    <div className="Index">
		      <div className="Moti-header">
		        <img src={logo} className="Moti-logo" alt="logo" />
		        <h2>Say hi to Moti!</h2>
		      </div>
		      <div className="Moti-box">
		      	<table class="table table-borderless">
		      		<tbody>
		      			<th scope="col"><img src={logo} className="Moti-logo" alt="logo" /></th>
		      			<th scope="col">If it is a particular Moti you wish to visit I would urge you to enter his digit!</th>
		      			<th scope="col"><img src={logo} className="Moti-logo" alt="logo" /></th>
		      		</tbody>
		      		<tbody>
		      			<td><img src={logo} className="Moti-logo" alt="logo" /></td>
		      			<td><Link to={this.state.id}><button class="btn btn-primary">Submit!</button></Link><Textbox updateNameHandler={this._updateId} /></td>
		      			<td><img src={logo} className="Moti-logo" alt="logo" /></td>
		      		</tbody>
		      	</table>
		    	</div> 
		    	<div className="Moti-list">
		    		<br/>
		 				<h5>A list of Moties you desire? then just that you shall acquire! </h5>
		 				<br/>
		 			</div>	
		 			<UsersList host={this.props.host} port={this.props.port}/>
		    </div>
      </div>
    );
  }
}


export default IndexPage;
