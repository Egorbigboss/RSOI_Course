import React, { Component } from 'react'
import { Link } from "react-router-dom";

export class Header extends Component {
    render() {
        return (
            <nav className="navbar navbar-expand-sm navbar-light bg-light">
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarTogglerDemo01">
              <a className="navbar-brand" href="#">Gateway</a>
              <ul className="navbar-nav mr-auto mt-2 mt-lg-0">
                <li className="nav-item">
                  <Link to="/cloths/" className="nav-link">Cloths</Link>
                </li>
                <li className="nav-item">
                  <Link to="/orders/" className="nav-link">Orders</Link>
                </li>
                <li className="nav-item">
                  <Link to="/delivery/" className="nav-link">Delivery List</Link>
                </li>
              </ul>
            </div>
          </nav>
        )
    }
}

export default Header
