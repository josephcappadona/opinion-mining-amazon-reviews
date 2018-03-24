import React, { Component } from 'react';
import './App.css';

// TODO(ryin): make API more sophisticated
import axios from 'axios';

// Components
import { Alignment, Navbar, NavbarDivider, NavbarGroup, NavbarHeading, Button, Search } from "@blueprintjs/core";

import { Card, Elevation } from "@blueprintjs/core";


class App extends Component {
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
              <input className="pt-input" type="search" placeholder="Search for a product..." dir="auto" />
            </div>
            <NavbarDivider />
            <Button className="pt-minimal" iconName="user"></Button>
            <Button className="pt-minimal" iconName="notifications"></Button>
            <Button className="pt-minimal" iconName="cog"></Button>
          </NavbarGroup>
        </Navbar>

        <ProductCardList/>
      </div>
    );
  }

}

class ProductCardList extends React.Component {
  constructor(props) {
    super(props)
    // set initial state
    this.state = {
      products: []
    }
  }

  componentDidMount() {
    const url = 'http://127.0.0.1:8000/products/'
    axios.get(url, {
      auth: {username: 'admin', password: 'password123'},
    })
    .then(res => {
      const products = res.data;
      this.setState({ products });
    })
    console.log('got data from api', this.state)
  }

  render() {
    const numProducts = this.state.products.length;
    const averageStarRating = this.state.products.reduce((sum, x) => sum + x, 0) / numProducts || null
    const starRatingStr = `| ${averageStarRating}/5 stars`
    const products = this.state.products.map((product) => {
      return <Card interactive={true} elevation={Elevation.TWO} key={product.id}>
        <h5><a href="#">{product.title}</a></h5>
        <p>{product.review_set.length} customer reviews{averageStarRating && starRatingStr}</p>
        <ProductQualityScores qualityScores={product.productqualityscore_set}/>
        <Button>Read More</Button>
      </Card>
    })

    return (
      <div className='product-list'>
        {products}
      </div>
    )
  }
}

function ProductQualityScores(props) {
  const qualityScores = props.qualityScores.map((quality_score) => {
    return <p>{quality_score.product_quality.name}: {quality_score.score}</p>
  })
  return (
    <div>
      {qualityScores}
    </div>
  )
}


export default App;
