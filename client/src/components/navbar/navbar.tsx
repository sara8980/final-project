import React, { FC } from 'react';
import './navbar.scss';
import { Link } from 'react-router-dom';
interface NavbarProps {}

const Navbar: FC<NavbarProps> = () => {
  return (
    <div className="Nav">
    <ul>
      <li><Link to="/homePage" className="link">Home page</Link></li>
      <li><Link to="/about" className="link">About</Link></li>
      <li><Link to="/image" className="link">Uploaded</Link></li>
    </ul>
  </div>
  );
  };
 export default Navbar;
