import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NavBarPage from './pages/NavBarPage';
import HomePage from './pages/HomePage';
import MusicRecommendationPage from './pages/MusicRecommendation';

function App() {
  const [isLoggedInSpotify, setIsLoggedInSpotify] = useState(false);

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<><NavBarPage isLoggedInSpotify={isLoggedInSpotify}/><HomePage setIsLoggedInSpotify={setIsLoggedInSpotify}/></>}/>
          <Route path="/music" element={<><NavBarPage isLoggedInSpotify={isLoggedInSpotify}/><MusicRecommendationPage setIsLoggedInSpotify={setIsLoggedInSpotify}/></>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;