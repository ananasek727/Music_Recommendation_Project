import HomePage from "../HomePage";
import React from 'react';
import {render, screen, fireEvent, act} from '@testing-library/react';
import {BrowserRouter} from 'react-router-dom';
import WebCamFrame from "../../components/WebCamFrame";


describe('HomePage', () => {
    afterEach(() => {
        jest.clearAllMocks();
    });
    it('renders correctly', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({data: []}),
            })
        );
        fetch.mockResolvedValueOnce({
            ok: true,
            json: () => ({url: "test"}),
        });
        await act(async () => {
            render(
                <BrowserRouter>
                    <HomePage setIsLoggedInSpotify={false}/>
                </BrowserRouter>
            );
        });
          const descriptionTextRegex = new RegExp(
    'Mus4You is an innovative music recommendation application designed to curate playlists tailored to your emotions, preferred genres, personalization level, and popularity preferences. With an intuitive interface and seamless integration with Spotify, Mus4You aims to elevate your music listening experience by delivering curated playlists that resonate with your mood and taste.'
          );
        // Ensure that the component renders without crashing
        expect(screen.getByText(descriptionTextRegex)).toBeInTheDocument();
    });
    it('handles Spotify login', async () => {
        global.fetch = jest.fn();

        global.fetch.mockImplementation((url) => {
            if (url === 'http://127.0.0.1:8000/get-auth-url') {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({url: 'test-url'}),
                });
            } else if (url === 'http://127.0.0.1:8000/access-token') {
                return Promise.resolve({
                    ok: false,
                    json: () => Promise.resolve({access_token: 'false'}),
                });
            }
        });
        await act(async () => {
            render(
                <BrowserRouter>
                    <HomePage />
                </BrowserRouter>
            );
        });
        await act(async () => {
            fireEvent.click(screen.getByText("Log in"));
        });

        expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/get-auth-url', {
            method: 'GET',
        });

    });
    it('handles token access', async () => {
        fetch.mockResolvedValueOnce({
            ok: true,
            json: () => ({url: "test"}),
        });
        await act(async () => {
            render(
                <BrowserRouter>
                    <HomePage setIsLoggedInSpotify={() => {
                    }}/>
                </BrowserRouter>
            );
        });
        expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/access-token', {
            method: 'GET',
        });
    });
});