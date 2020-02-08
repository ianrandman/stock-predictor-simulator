import React from 'react';
import { Link } from 'react-router-dom';

import './NavBar.css';

const NavBar = () => {
  return (
    <div className='NavBar'>
      <h5>NAVBAR</h5>
      <ul>
        <li><Link to="/Home">Home</Link></li>
        <li><Link to="/About">About</Link></li>
      </ul>
      <hr />
    </div>
  );
};

export default NavBar;