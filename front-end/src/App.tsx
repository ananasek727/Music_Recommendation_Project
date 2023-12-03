import React from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NavBarPage from './pages/NavBarPage';
import HomePage from './pages/HomePage';
import MusicRecommendationPage from './pages/MusicRecommendation';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<><NavBarPage/><HomePage/></>}/>
          <Route path="/music" element={<><NavBarPage/><MusicRecommendationPage/></>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;