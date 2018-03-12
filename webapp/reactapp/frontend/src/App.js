import React, { Component } from 'react';
import './App.css';

// TODO(ryin): make API more sophisticated
import axios from 'axios';

// Components
import { Alignment, Navbar, NavbarDivider, NavbarGroup, NavbarHeading, Button, Search } from "@blueprintjs/core";

import { Card, Elevation } from "@blueprintjs/core";


class App extends Component {

  constructor(props) {
    super(props)
    this.state = {products: [{'id': -1}]}
    const url = 'http://127.0.0.1:8000/products/'
    // curl -H 'Accept: application/json; indent=4' -u admin:password123 
    axios.get(url, {
      auth: {username: 'admin', password: 'password123'},
    })
    .then(res => {
        const products = res.data;
        this.setState({ products });
    })

    this.renderProducts = this.renderProducts.bind(this)
  }

  renderProducts() {
    return this.state.products.map((product, index) => {
      <Card interactive={true} elevation={Elevation.TWO}>
        <h5><a href="#">{product.title}</a></h5>
        <p>1,169 customer reviews | 4.0/5 stars</p>
        <Button>Read More</Button>
      </Card>
    })
  }

  render() {
    return (
      <div>
        <Navbar>
          <NavbarGroup>
            <NavbarHeading>Amazon Review Aggregator</NavbarHeading>
          </NavbarGroup>
          <NavbarGroup>
            <Button className="pt-minimal" iconName="home"></Button>
            
            <div className="pt-input-group .modifier">
              <span className="pt-icon pt-icon-search"></span>
              <input className="pt-input" modifier type="search" placeholder="Search for a product..." dir="auto" />
            </div>
            <NavbarDivider />
            <Button className="pt-minimal" iconName="user"></Button>
            <Button className="pt-minimal" iconName="notifications"></Button>
            <Button className="pt-minimal" iconName="cog"></Button>
          </NavbarGroup>
        </Navbar>

        <Card interactive={true} elevation={Elevation.TWO}>
          <h5><a href="#">{this.state.products[0].title}</a></h5>
          <p>1,169 customer reviews | 4.0/5 stars</p>
          <Button>Read More</Button>
        </Card>

        {this.state.products.map(product => {
          <Card interactive={true} elevation={Elevation.TWO}>
            <h5><a href="#">{product.title}</a></h5>
            <p>1,169 customer reviews | 4.0/5 stars</p>
            <Button>Read More</Button>
          </Card>
        })}
      </div>
    );
  }

}

export default App;
