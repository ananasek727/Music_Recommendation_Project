import HomePage from "../HomePage";
import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Manually mock the fetch function
global.fetch = jest.fn();

describe('HomePage', () => {
  afterEach(() => {
    // Clear the mock calls between tests
    jest.clearAllMocks();
  });
  it('renders correctly', async () => {
    render(
      <BrowserRouter>
        <HomePage setIsLoggedInSpotify={() => {}} />
      </BrowserRouter>
    );

    // Ensure that the component renders without crashing
    expect(screen.getByText(/Description/i)).toBeInTheDocument();
  });
  it('handles Spotify login',  () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => ({ url: "test" }),
    });

    render(
      <BrowserRouter>
        <HomePage setIsLoggedInSpotify={() => {}} />
      </BrowserRouter>
    );
    fireEvent.click(screen.getByText("Log in"));

    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/get-auth-url', {
      method: 'GET',
    });
  });
    it('handles token access',  () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => ({ url: "test" }),
    });

    render(
      <BrowserRouter>
        <HomePage setIsLoggedInSpotify={() => {}} />
      </BrowserRouter>
    );
    fireEvent.click(screen.getByText("Log in"));
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/access-token', {
      method: 'GET',
    });
  });
});