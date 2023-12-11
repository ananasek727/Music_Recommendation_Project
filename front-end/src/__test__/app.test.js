
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import App from '../App';

test('renders App component', () => {
  render(<App />);
});

test('renders home page', () => {
  render(<App />);
  expect(screen.getByText('Description')).toBeInTheDocument(); // Adjust text as per your actual content
});
test('renders navBar', () => {
  render(<App />);
  expect(screen.getByText('Mus4You')).toBeInTheDocument(); // Adjust text as per your actual content
});

