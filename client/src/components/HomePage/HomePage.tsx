import React, { FC } from 'react';
import './HomePage.scss';
import Nav from '../navbar/navbar'
import Logo from '../Logo/Logo';
interface HomePageProps {}

const HomePage: FC<HomePageProps> = () => {
  return (
    
    <div className="homePage">
       <div className="navContainer">
        <Nav />
      </div>
     <div className='container' >   
     
     <h1>Welcome to Age Classifier</h1>
     <p>Precise Image Age Classification</p>
     <section className="services">
        <h2>Our Services</h2>
        <ul>
          <li>
            <strong>Automated Age Detection:</strong> Upload any image and instantly determine the age group depicted.
          </li>
          <li>
            <strong>Age Group Filtering:</strong> Automatically categorize images based on age, ensuring privacy and security.
          </li>
          <li>
            <strong>Privacy Assurance:</strong> We prioritize your privacy. Our classification results are not stored or shared after use.
          </li>
        </ul>
        <section className="how-it-works">
        <h2>How It Works</h2>
        <p>Simply visit our platform, upload an image, and receive immediate, precise age classification results.</p>
      </section>
      </section>
      <Logo></Logo>
      </div>
     
    
    </div>
  );
};


export default HomePage;
