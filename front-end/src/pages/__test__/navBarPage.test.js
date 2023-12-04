import {shallow} from 'enzyme';
import {configure, simulate, text} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import NavBarPage from "../NavBarPage";
import React from 'react';
import {render, screen} from '@testing-library/react';
configure({adapter: new Adapter()});
import { BrowserRouter as Router } from 'react-router-dom';
  it('renders Navbar with title "Mus4You"', () => {
    render(
      <Router>
        <NavBarPage />
      </Router>
    );

    // Assert that the title "Mus4You" is present in the rendered component
    expect(screen.getByText('Mus4You')).toBeInTheDocument();
  });

  it('does not render Home button when not on the /music route', () => {
    // Mock useLocation to return a pathname other than '/music'
    jest.mock('react-router-dom', () => ({
      ...jest.requireActual('react-router-dom'),
      useLocation: () => ({
        pathname: '/some-other-route',
      }),
    }));

    render(
      <Router>
        <NavBarPage />
      </Router>
    );

    // Assert that the Home button is not rendered when not on the /music route
    expect(screen.queryByText('Home')).toBeNull();
  });