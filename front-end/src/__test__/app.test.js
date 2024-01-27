
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from '../App';

test('renders App component', () => {
  render(<App />);
});

test('renders home page', () => {
  render(<App />);
  const descriptionTextRegex = new RegExp(
    'Mus4You is an innovative music recommendation application designed to curate playlists tailored to your emotions, preferred genres, personalization level, and popularity preferences. With an intuitive interface and seamless integration with Spotify, Mus4You aims to elevate your music listening experience by delivering curated playlists that resonate with your mood and taste.'
  );
  expect(screen.getByText(descriptionTextRegex)).toBeInTheDocument();});
test('renders navBar', () => {
  render(<App />);
  expect(screen.getByText('Mus4You')).toBeInTheDocument(); // Adjust text as per content
});

