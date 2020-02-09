import React from 'react';
import NavBar from "../components/NavBar";

const NoMatch = (props) => {
  return (
    <div>
      <NavBar pageName='404'/>
      <h1>404 PAGE NOT FOUND</h1>
    </div>
  );
};

export default NoMatch;