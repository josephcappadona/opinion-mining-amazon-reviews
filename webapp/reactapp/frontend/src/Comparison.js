import React, { Component } from 'react'
import './App.css'

// TODO(ryin): make API more sophisticated
import axios from 'axios'
import _ from 'lodash'

import './Comparison.css'

// Components
import { Alignment, Navbar, NavbarDivider, NavbarGroup, NavbarHeading, Button, Search } from "@blueprintjs/core"

import { Card, Elevation } from "@blueprintjs/core"


class Comparison extends Component {
  constructor(props) {
    super(props)
    // set initial state
    this.state = {
      products: [],
    }
  }

  componentDidMount() {
    const url = 'http://127.0.0.1:8000/products'
    axios.get(url, {
      auth: {username: 'admin', password: 'password123'},
      params: {compare: 'B06ZYX6Y1T,B00STP86HC,B00E4LGVUO'},
    })
    .then(res => {
      const products = res.data
      this.setState({ products })
    })
  }

  render() {
    const numProducts = this.state.products.length
    const averageStarRating = this.state.products.reduce((sum, x) => sum + x, 0) / numProducts || null
    const starRatingStr = `| ${averageStarRating}/5 stars`

    const productIdToPQs = this.state.products.reduce((acc, product) => {
      acc[product.id] = {}
      for (var pq of product.productqualityscore_set) {
        acc[product.id][pq.product_quality.name] = pq.score
      }
      return acc
    }, {})

    // NB(ryin): MESSY JAVASCRIPT TO GROUP BY PQs. We do this client side so that users can add their
    // own PQs and not have to reload page.

    const allPQs = new Set()
    const pqCounts = this.state.products.reduce((acc, product) => {
      for (var pq of product.productqualityscore_set) {
        const name = pq.product_quality.name
        if (!acc.hasOwnProperty(name)) acc[name] = 0
        acc[name]++
        allPQs.add(name)
      }
      return acc
    }, {})

    const sortedPQs = [...allPQs] // convert to Array
    _.sortBy(sortedPQs, (pqName) => pqCounts[pqName])

    // Make rows for each PQ

    const rowsData = sortedPQs.map((pqName) => {
      return {
        name: pqName,
        productScores: this.state.products.map((prod) => (productIdToPQs[prod.id][pqName] || '-'))
      }
    })

    const productNames = this.state.products.map((prod) => prod.title)
    return (
      <div>
        <table className="pt-html-table pt-interactive compare-table">
          <ProductQualityHeader productNames={productNames}/>
          
          <tbody>
            {rowsData.map((row) => <ProductQualityRow name={row.name} productScores={row.productScores}/>)}
          </tbody>

        </table>
      </div>
    )
  }
}

const ProductQualityHeader = props => {
  return <thead className="compare-table-header">
    <tr>
      <th>Product Quality</th>
      {props.productNames.map((name) => <th key={name}>{name}</th>)}
    </tr>
  </thead>
}

const ProductQualityRow = props => {
  // name: name of pq
  // productScores: [score]
  return (
    <tr>
      <td>{props.name}</td>
      {
        props.productScores.map((score, index) => (<td key={index}>{score}</td>))
      }
    </tr>
  )
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

export default Comparison
