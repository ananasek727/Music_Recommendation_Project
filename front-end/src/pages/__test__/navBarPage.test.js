import React from 'react';
import {render, screen, fireEvent, waitFor} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import NavBarPage from '../NavBarPage';
import {BrowserRouter} from "react-router-dom";

global.fetch = jest.fn(() =>
    Promise.resolve({
        ok: true,
        json: () => Promise.resolve({url: 'test', data: 'data'}),
    })
);

describe('NavBarPage component', () => {
    it('renders without crashing', () => {
        render(<BrowserRouter>
            <NavBarPage isLoggedInSpotify={true}/>
        </BrowserRouter>);
        expect(screen.getByText('Mus4You')).toBeInTheDocument();
    });

    it('renders the "Logout" button when isLoggedInSpotify is true', () => {
        render(<BrowserRouter>
            <NavBarPage isLoggedInSpotify={true}/>
        </BrowserRouter>);
        expect(screen.getByText('Logout')).toBeInTheDocument();
    });

    it('does not render the "Logout" button when isLoggedInSpotify is false', () => {
        render(<BrowserRouter>
            <NavBarPage isLoggedInSpotify={false}/>
        </BrowserRouter>);
        expect(screen.queryByText('Logout')).not.toBeInTheDocument();
    });

    it('calls the handleLogOut function when "Logout" button is clicked', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({data: []}),
            })
        );
        await waitFor(async () => {
            render(<BrowserRouter>
                <NavBarPage isLoggedInSpotify={true}/>
            </BrowserRouter>)
        });
        const logoutButton = screen.getByText('Logout');
        fireEvent.click(logoutButton);
        expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/logout', {
            method: 'DELETE',
        });
    });
});
