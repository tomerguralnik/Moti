import React, { Component } from 'react';
import logo from './logo.png';
import './UserPage.css';
class UserPage extends Component{
	state = {
		snapshots: [],
		user: null
	}
	componentDidMount(){
		var user = `http://${window.api_host}:${window.api_port}/users/${this.props.match.params.id}`;
		fetch(user).then(response => response.json()).then(this._updateUser);
		fetch(user + "/snapshots").then(snapshots => snapshots.json()).then(this._updateSnapshots);
	}

	_updateUser = user => {
		this.setState({'user': user});
	}

	_updateSnapshots = snapshots => {
		this.setState({'snapshots': snapshots});
	}

	render(){
		if (this.state.user == null){
			return <p>loading...</p>; 
		}
		return (
			<div class="User">
				<div className="Moti-header">
		        	<img src={logo} className="Moti-logo" alt="logo" />
		        	<h2>Say hi to Moti {this.state.user.ID}!</h2>
		      	</div>
				<div className="Moti-intro">
					<h2>I'm moti {this.state.user.ID}</h2>
					<User birthday={this.state.user.birthday} name={this.state.user.name} id={this.state.user.ID} gender={this.state.user.gender}/> 
				</div>	
				<div>
					<table class="table table-striped table-bordered mx-auto">
						<thead class="thead-dark">
							<th scope="col"/>
							<th scope="col">#</th>
							<th scope="col">Description</th>
							<th scope="col"/>
						</thead>
						<tbody>	
							{this.state.snapshots.map((snap) => <SnapshotLink snapshot={snap} user={this.state.user.ID} />)}
						</tbody>
					</table>
				</div>		
			</div>
			);
	}
}

class User extends Component{
	render(){
		var birthdate = new Date(1970, 0, 1);
		birthdate.setSeconds(this.props.birthday);
		var birthstr = `${birthdate.getDate()}.${birthdate.getMonth() + 1}.${birthdate.getYear()}`
		var gender = this.props.gender == 'm' ? 'male': 'female'; 
		return (
			<p>
				Hi! my name is {this.props.name}, I am moti number {this.props.id}<br />
				I was concieved at {birthstr}, And technichally a {gender}
			</p>); 	
	}
}

class SnapshotLink extends Component{
	render(){
		var time = new Date(1970, 0, 1);
		time.setMilliseconds(this.props.snapshot.timestamp);
		var timestr = `${time.getDate()}.${time.getMonth() + 1}.${time.getYear()}`;
		return (<tr>
				<th scope="row"><a href={this.props.user+"/"+this.props.snapshot.ID} class="btn btn-primary">Look at this!</a></th>
			 	<td>{this.props.snapshot.ID}</td> 
			 	<td>Wondering what I did at {timestr} are we?</td>
			 	<td><img src={logo} className="Small-logo" alt="logo" /></td>
			</tr>);
	}
}

export default UserPage