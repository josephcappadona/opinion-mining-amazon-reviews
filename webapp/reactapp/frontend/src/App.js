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

const SiteNavbar = () => (
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
          <form method = "GET" action = "/search">
            <input name = "q" className="pt-input" type="search" placeholder="Search for a product..." dir="auto" />
            <button type="submit" class="pt-button pt-icon-add .modifier">Button</button>
          </form>
        </div>
        <NavbarDivider />
        <Button className="pt-minimal" iconName="user"></Button>
        <Button className="pt-minimal" iconName="notifications"></Button>
        <Button className="pt-minimal" iconName="cog"></Button>
      </NavbarGroup>
    </Navbar>

    <div>
      <Route exact path="/" component={ProductList} />
      <Route path="/compare/:id1/:id2" component={Comparison} />
    </div>
  </div>
)

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

