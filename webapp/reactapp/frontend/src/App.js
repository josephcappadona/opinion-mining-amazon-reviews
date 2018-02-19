import React, { Component } from 'react';
import './App.css';


import { Alignment, Navbar, NavbarDivider, NavbarGroup, NavbarHeading, Button, Search } from "@blueprintjs/core";

import { Card, Elevation } from "@blueprintjs/core";


class App extends Component {
  render() {
    return (
      <div>
        <Navbar>
          <NavbarGroup>
            <NavbarHeading>Review Aggregator</NavbarHeading>
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
          <h5><a href="#">Arctix Men's Essential Snow Pants</a></h5>
          <p>1,169 customer reviews | 4.0/5 stars</p>
          <Button>Read More</Button>
      </Card>

      <Card interactive={true} elevation={Elevation.TWO}>
          <h5><a href="#">Arctix Men's Essential Snow Pants</a></h5>
          <p>1,169 customer reviews | 4.0/5 stars</p>
          <Button>Read More</Button>
      </Card>

      <Card interactive={true} elevation={Elevation.TWO}>
          <h5><a href="#">Arctix Men's Essential Snow Pants</a></h5>
          <p>1,169 customer reviews | 4.0/5 stars</p>
          <Button>Read More</Button>
      </Card>

      </div>
    );
  }
}

export default App;
