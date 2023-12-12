import React from 'react';
import {render, screen} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import MusicControl from '../MusicControl';

const mockProps = {
  playlist: {
    data: [{
        title: 'Example Song',
        artist_str: 'Example Artist',
        duration: 240, // Duration in seconds (4 minutes)
        image_url: 'https://example.com/song-image.jpg',
        id: '123456789', // Unique identifier for the song
        uri: 'spotify:track:abcdefg123456', // Spotify URI for the song
    }],
  },
  recommendedPlaylist: [], // Mock recommendedPlaylist as needed
  playlistSongsURI: [], // Mock playlistSongsURI as needed
  isPlaylistEmpty: false, // Mock isPlaylistEmpty as needed
  playlistChangeGuard: jest.fn(), // Mock playlistChangeGuard as needed
  setIsLoggedInSpotify: jest.fn(), // Mock setIsLoggedInSpotify as needed
};
describe('MusicControl Component', () => {
  it('renders without crashing', () => {
    render(<MusicControl {...mockProps} />);
  });
  it('renders music controlel', () => {
    render(<MusicControl {...mockProps} />);
    const musicControler = screen.getByText('Play track');
    expect(musicControler).toBeInTheDocument();
  });

  it('renders playlist element', () => {
    render(<MusicControl {...mockProps} />);
    const playlistElement = screen.getByTestId('playlist-element');
    expect(playlistElement).toBeInTheDocument();
  });
});
