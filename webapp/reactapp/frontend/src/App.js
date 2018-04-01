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
      search: '',
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
            <Link to="/compare">
              <Button className="pt-minimal" iconName="comparison"></Button>
            </Link>

            <Link to="/">
              <Button className="pt-minimal" iconName="home"></Button>
            </Link>

            <div className="pt-input-group .modifier">
              <span className="pt-icon pt-icon-search"></span> 
              <form method = "GET">
                <input style={{'paddingLeft': '30px'}} value={this.state.search} name = "search" className="pt-input" type="search" placeholder="Search" dir="auto" onChange={this.handleChange}/>
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
          <Route path="/compare" component={Comparison} />
        </div>
      </div>
    )
  }

  handleChange(event) {
    this.setState({search: event.target.value});
  }

  // handleSubmit(event) {
  //   // alert('A name was submitted: ' + this.state.search);

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

