import React from 'react';
import {render, screen, fireEvent, waitFor} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect'; // for expect(...).toBeInTheDocument()
import MusicControlPanel from '../MusicControlPanel';
describe('MusicControlPanel Component', () => {
  beforeEach(() => {
    jest.spyOn(global, 'fetch').mockImplementation(() => Promise.resolve({
      json: () => Promise.resolve({}),
      ok: true,
    }));
  });
  const mockProps = {
    setIsLoggedInSpotify: true,
    playlistChangeGuard: false,
    playlistSongsURI: ["song1"],
    isPlaylistEmpty: false,
    isSongPlayed: true,
    currentSong: {
      title: 'Test',
      artist: 'Test',
      duration: '3:30',
      time_stamp: '12:00',
      image_url: 'test_url',
      is_playing: true,
      id: '123',
      uri: 'url',
    }
  };

  it('renders without crashing', () => {
    render(<MusicControlPanel {...mockProps} />);
  });

  it('displays Play track button when no song is played', () => {
    render(<MusicControlPanel {...mockProps} />);
    const playButton = screen.getByText('Play track');
    expect(playButton).toBeInTheDocument();
  });

  it('displays Next track button', () => {
    render(<MusicControlPanel {...mockProps} />);
    const nextButton = screen.getByText('Next track');
    expect(nextButton).toBeInTheDocument();
  });

  it('displays a volume slider', () => {
    render(<MusicControlPanel {...mockProps} />);
    const volumeSlider = screen.getByTestId('volume-slider');
    expect(volumeSlider).toBeInTheDocument();
  });

  test('Play button is disabled when playlist is empty', () => {
  render(<MusicControlPanel isPlaylistEmpty={true} />);
  const playButton = screen.getByText('Play track');
  expect(playButton).toBeDisabled();
});
test('Next Track button is disabled when playlist is empty', () => {
  render(<MusicControlPanel isPlaylistEmpty={true} />);
  const nextTrackButton = screen.getByText('Next track');
  expect(nextTrackButton).toBeDisabled();
});
  it('fetches access token on mount', async () => {
    render(<MusicControlPanel />);
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/access-token', { method: 'GET' }));
  });

    it('calls nextTrack function when Next Track button is clicked', async () => {
    render(<MusicControlPanel />);
    const nextTrackButton = screen.getByText('Next track');
    fireEvent.click(nextTrackButton);
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/player/next', expect.any(Object)));
  });

  it('calls changeVolume function when volume slider is adjusted', async () => {
    render(<MusicControlPanel />);
    const volumeSlider = screen.getByTestId('volume-slider');
    fireEvent.change(volumeSlider, { target: { value: 75 } });
    fireEvent.mouseUp(volumeSlider);
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/player/set-volume', expect.any(Object)));
  });
});
