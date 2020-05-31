import React, { Component } from 'react';
import logo from './logo.png';
import './IndexPage.css';
import $ from "jquery";
class UserLink extends Component{
	render(){
		return (<tr>
			<th scope="row"><a href={this.props.id} class="btn btn-primary">Visit me!</a> </th>  
			<td>{this.props.id}</td>
			<td> is a very nice Moti, he likes to be reffered to as {this.props.name}</td>
			<td><img src={logo} className="Small-logo" alt="logo" /></td>
		</tr>);
	}
}

class UsersList extends Component{
	state = {
		list: []
	}
	_updateList = data => {
		this.setState({list: data});
	}
	componentDidMount(){
		fetch(`http://${window.api_host}:${window.api_port}/users`).then(response => response.json()).then(this._updateList);
	}
	render(){
		return (<div><table class="table table-striped table-bordered mx-auto">
				<thead class="thead-dark">
					<th scope="col"></th>
					<th scope="col">#</th>
					<th scope="col">Description</th>
					<th scope="col"/>
				</thead>
				<tbody>
					{this.state.list.map((user) => <UserLink id={user.ID} name={user.Name} />)}
				</tbody>
			</table></div>);
	}
}

export {UserLink};
export {UsersList};