import React from 'react';
import {render, screen} from '@testing-library/react';
import PlaylistElement from '../PlaylistElement';

describe('PlaylistElement', () => {
    const sampleSong = {
        title: 'Sample Title',
        artist: 'Sample Artist',
    };

    test('renders playlist element with correct song title and artist', () => {
        render(<PlaylistElement song={sampleSong}/>);
        const titleElement = screen.getByText(sampleSong.title);
        const artistElement = screen.getByText(sampleSong.artist);

        expect(titleElement).toBeInTheDocument();
        expect(artistElement).toBeInTheDocument();
    });

});