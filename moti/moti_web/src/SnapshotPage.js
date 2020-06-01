import React, { Component } from 'react';
import exhaustionImage from './exhaustionImage.jpg'
import happinessImage from './happinessImage.jpg'
import hungerImage from './hungerImage.jpg'
import thirstImage from './thirstImage.jpg'
import logo from './logo.png';
import './SnapshotPage.css';
class SnapshotPage extends Component{
	render(){
		return (
			<div class="Snapshot">
				<div className="Moti-header">
		        	<img src={logo} className="Moti-logo" alt="logo" />
		        	<h2>Say hi to Moti!</h2>
		     	</div>
				<div className="Feelings">
					<div className="FeelingsText">
						<h3>And I'm Feeeeelin'....</h3>
					</div>
					<div className="FeelingsShow">
						<Feelings id={this.props.match.params.id} snapshot={this.props.match.params.snapshot}/>
					</div>
				</div>
				<div className="Pose">
					<div className="PoseText">
						<h2>Are you following me?!</h2>
					</div>
					<Pose id={this.props.match.params.id} snapshot={this.props.match.params.snapshot}/>
				</div>
				<div className="Images">
					<table class="table table-borderless">
						<thead>
							<th>You can see what I see?<br/>This is getting creepy...</th>
							<th>Not exactly sure what this is though</th>
						</thead>
						<tbody>
							<td><ColorImage id={this.props.match.params.id} snapshot={this.props.match.params.snapshot}/></td>
							<td><DepthImage id={this.props.match.params.id} snapshot={this.props.match.params.snapshot}/></td>
						</tbody>
					</table>
				</div>
			</div>
			);
	}
}

class ColorImage extends Component{
	state = {
		image: null
	};

	_updateImage = image => {
		this.setState({'image': image});
	} 
	componentDidMount(){
		var url = `http://${window.api_host}:${window.api_port}/users/${this.props.id}/snapshots/${this.props.snapshot}/color_image`;
		fetch(url).then(response => response.json()).then(json => json.color_image_url).then(image => {
				fetch(image).then(response => response.blob()).then(blob => URL.createObjectURL(blob)).then(this._updateImage);
			});	
	}	
	render(){	
		if (this.state.image == null){
			return <p>loading...</p>
		}
		return <img src={this.state.image} width="500" height="250"/>
	}
}

class DepthImage extends Component{
	state = {
		image: null
	}
	_updateImage = image => {
		this.setState({'image': image});
	} 
	componentDidMount(){
		var url = `http://${window.api_host}:${window.api_port}/users/${this.props.id}/snapshots/${this.props.snapshot}/depth_image`;
		fetch(url).then(response => response.json()).then(json => json.depth_image_url).then(image => {
				fetch(image).then(response => response.blob()).then(blob => URL.createObjectURL(blob)).then(this._updateImage);
			});	
	}	
	render(){	
		if (this.state.image == null){
			return <p>loading...</p>
		}
		return <img src={this.state.image} width="480" height="360" />
	}
}

class Feelings extends Component{
	state = {
		hunger: null,
		thirst: null,
		exhaustion: null,
		happiness: null
	}
	_updateFeelings = feelings => {
		this.setState(feelings.feelings)
	}
	componentDidMount(){
		var url = `http://${window.api_host}:${window.api_port}/users/${this.props.id}/snapshots/${this.props.snapshot}/feelings`;
		fetch(url).then(response => response.json()).then(this._updateFeelings);
	}
	render(){
		if (this.state.hunger == null){
			return <p>loading...</p>
		}
		return (
			<div className="FeelingsImages">
				<table class="table table-bordered">
					<thead class="thead-dark">
						<th scope="col"/>
						<th scope="col">Hunger</th>
						<th scope="col">Thirst</th>
						<th scope="col">Exhaustion</th>
						<th scope="col">happiness</th>
					</thead>
					<tbody>
						<tr>
							<th scope="row">Numeric value</th>
							<td>{this.state.hunger}</td>
							<td>{this.state.thirst}</td>
							<td>{this.state.exhaustion}</td>
							<td>{this.state.happiness}</td>
						</tr>
						<tr>
							<th scope="row">Visual representation</th>
							<td><img src={hungerImage} width="120" height="120" opacity={this.state.hunger}/></td>
							<td><img src={thirstImage} width="120" height="120" opacity={this.state.thirst}/></td>
							<td><img src={exhaustionImage} width="120" height="120" opacity={this.state.exhaustion}/></td>
							<td><img src={happinessImage} width="200" height="120" opacity={this.state.happiness}/></td>
						</tr>
					</tbody>
				</table>
			</div>
			);
	}
}

class Pose extends Component{
	state = {
		translation: null,
		rotation: null,
		translation_picture_url: null,
		image: null
	}
	_updatePose = pose => {
		this.setState({translation: pose.pose.translation, rotation: pose.pose.rotation, translation_picture_url: pose.translation_picture_url})
		fetch(this.state.translation_picture_url).then(response => response.blob()).then(blob => URL.createObjectURL(blob)).then(this._updateImage);
	}
	_updateImage = image => {
		this.setState({'image': image})
	}
	componentDidMount(){
		var url = `http://${window.api_host}:${window.api_port}/users/${this.props.id}/snapshots/${this.props.snapshot}/pose`;
		fetch(url).then(result => result.json()).then(this._updatePose)
		fetch(this.state.translation_picture_url).then(response => response.blob()).then(blob => URL.createObjectURL(blob)).then(this._updateImage);
	}
	render(){
		if(this.state.image == null){
			return <p>loading...</p>
		}
		return (
			<div>
				<table class="table table-bordered">
					<thead class="thead-dark">
						<th scope="col"/>
						<th scope="col">x</th>
						<th scope="col">y</th>
						<th scope="col">z</th>
						<th scope="col">w</th>
						<th scope="col">Visualization</th>
					</thead>
					<tbody>
						<tr>
							<th scope="row">Translation</th>
							<td>{this.state.translation.x}</td>
							<td>{this.state.translation.y}</td>
							<td>{this.state.translation.z}</td>
							<td><img src={logo} className="Moti-logo" alt="logo" /></td>
							<td><img src={this.state.image} className="Pose-Pic"/></td>
						</tr>
						<tr>
							<th scope="row" class="text-center">Rotation</th>
							<td>{this.state.rotation.x}</td>
							<td>{this.state.rotation.y}</td>
							<td>{this.state.rotation.z}</td>
							<td>{this.state.rotation.w}</td>
							<td><img src={logo} className="Moti-logo" alt="logo" /></td>
						</tr>
					</tbody>
				</table>
			</div>
			);
	}
}
export default SnapshotPage