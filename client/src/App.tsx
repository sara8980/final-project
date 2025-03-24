import React from 'react';
import logo from './logo.svg';
import './App.scss';
import axios from 'axios';
import YourImage from './components/UploadPicture/UploadPicture';
import  Navbar  from './components/navbar/navbar';
import { BrowserRouter, Route,Routes } from 'react-router-dom';
import FamilyTree from './components/Ages-tree/Ages-tree';
import NotFound from './components/NotFound/NotFound';
import HomePage from './components/HomePage/HomePage';
import AboutPage from './components/AboutPage/AboutPage';
function App() {


  return <Routes>
      <Route path='/' element={<HomePage />} />
      <Route path='/image' element={<YourImage />} />
      <Route path='/about' element={<AboutPage />} />
      <Route path='/homePage' element={<HomePage />} />
      {/* <Route path='/family-tree' element={<FamilyTree file={} />} /> */}
      <Route path='*' element={<NotFound></NotFound>}></Route>
    </Routes>
}

export default App;
