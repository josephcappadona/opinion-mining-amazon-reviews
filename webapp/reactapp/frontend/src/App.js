import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom"


// CSS
import './App.css';

// Components

// OURS
import ProductList from './ProductList'
import Comparison from './Comparison'

// BLUEPRINT
import { Navbar, NavbarDivider, NavbarGroup, NavbarHeading, Button, Search } from "@blueprintjs/core";

class SiteNavbar extends Component {
  constructor(props) {
    super(props)
    // set initial state
    this.state = {
      q: '',
    }
    this.handleChange = this.handleChange.bind(this)
  }

  render() {
    return (
      <div>
        <Navbar>
          <NavbarGroup>
            <NavbarHeading>Amazon Review Aggregator</NavbarHeading>
          </NavbarGroup>
          <NavbarGroup className="navbarSettings">
            <Link to="/compare/1/2">
              <Button className="pt-minimal" iconName="comparison"></Button>
            </Link>

            <Link to="/">
              <Button className="pt-minimal" iconName="home"></Button>
            </Link>

            <div className="pt-input-group .modifier">
              <span className="pt-icon pt-icon-search"></span> 
              <form method = "GET">
                <input style={{'padding-left': '30px'}}value={this.state.q} name = "q" className="pt-input" type="search" placeholder="Search" dir="auto" onChange={this.handleChange}/>
                <input type="submit" style={{display: 'none'}}/>
              </form>
            </div>
            <NavbarDivider />
            <Button className="pt-minimal" iconName="user"></Button>
            <Button className="pt-minimal" iconName="notifications"></Button>
            <Button className="pt-minimal" iconName="cog"></Button>
          </NavbarGroup>
        </Navbar>

        <div>
          <Route exact path="/" component={ProductList}/>
          <Route path="/compare/:id1/:id2" component={Comparison} />
        </div>
      </div>
    )
  }

  handleChange(event) {
    this.setState({q: event.target.value});
  }

  // handleSubmit(event) {
  //   // alert('A name was submitted: ' + this.state.q);

  //   event.preventDefault();
  // }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <SiteNavbar/>
        </Router>
      </div>
    )
  }
}

export default App

