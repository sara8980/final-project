
import React, { useState } from 'react';
import './AboutPage.scss';
import Nav from '../navbar/navbar'
import Logo from '../Logo/Logo';

const AboutPage = () => {
  const [image, setImage] = useState(null);

  
  return (
    <div>
      <div>
        <Nav />
      </div>
    <div className="aboutPage">
    <h2>About Us</h2>
      <p>Welcome to our Age Classifier platform! We are dedicated to providing innovative solutions that celebrate life's stages and connections.</p>
      
      <p>Our website offers a unique service - utilizing advanced algorithms to analyze and classify age groups. Whether you're interested in understanding generational shifts or simply exploring the passage of time, our platform offers insightful perspectives.</p>

      <h2>How it Works</h2>
      <ol>
        <li><strong>Upload an Image:</strong> Use the upload feature to submit an image.</li>
        <li><strong>Age Classification:</strong> Our algorithm will analyze the image and categorize individuals by age groups.</li>
        <li><strong>Explore Insights:</strong> Gain insights into demographic trends or personal milestones based on the analysis provided.</li>
      </ol>

      <p>Join us in exploring the richness of age diversity and the stories it tells. Discover how our platform can illuminate the journey of life.</p>
      <Logo></Logo>
    </div>
   
    </div>
  );
};

export default AboutPage;
