import React, { FC } from 'react';
import './Logo.scss';
import myImage from '../../images/image (8).png'; // תיבא את התמונה שלך
import '../Logo/Logo.scss'; // קוב
interface LogoProps {}

const Logo: FC<LogoProps> = () => {
  return (
    <div className="image-container">
      <img src={myImage} className="centered-image" alt="My Image" />
    </div>
  );
};

export default Logo;
