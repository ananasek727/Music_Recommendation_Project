import PlaylistElement from '../PlaylistElement';
import React from 'react';
import { render } from '@testing-library/react';

describe('PlaylistElement Component', () => {
  const song = {
    title: 'song',
    artist_str: 'artist',
    image_url: 'url',
  };

  it('renders without crashing', () => {
    render(<PlaylistElement song={song} />);
  });

  it('renders the song title correctly', () => {
    const { getByText } = render(<PlaylistElement song={song} />);
    expect(getByText(song.title)).toBeInTheDocument();
  });

  it('renders the artist correctly', () => {
    const { getByText } = render(<PlaylistElement song={song} />);
    expect(getByText(song.artist_str)).toBeInTheDocument();
  });

  it('renders the image correctly', () => {
    const { getByRole } = render(<PlaylistElement song={song} />);
    expect(getByRole("img")).toHaveAttribute('src', song.image_url);
  });

  it('applies the correct font size and weight to the title', () => {
    const { getByText } = render(<PlaylistElement song={song} />);
    const title = getByText(song.title);
    expect(title).toHaveStyle({ fontSize: '20px', fontWeight: 'bold' });
  });

  it('applies the correct font size to the artist', () => {
    const { getByText } = render(<PlaylistElement song={song} />);
    const artist = getByText(song.artist_str);
    expect(artist).toHaveStyle({ fontSize: '15px' });
  });

  it('applies the correct frame class', () => {
    const { container } = render(<PlaylistElement song={song} />);
    expect(container.firstChild).toHaveClass('PlaylistElementFrame');
  });

  it('applies the correct left side class', () => {
    const { container } = render(<PlaylistElement song={song} />);
    expect(container.firstChild.firstChild).toHaveClass('PlaylistElementLeft');
  });

  it('applies the correct right side class', () => {
    const { container } = render(<PlaylistElement song={song} />);
    expect(container.firstChild.lastChild).toHaveClass('PlaylistElementRight');
  });
});