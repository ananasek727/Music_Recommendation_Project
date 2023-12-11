import MusicParameters from "../MusicParameters";
import React from 'react';
import {render, fireEvent, waitFor} from '@testing-library/react';


describe('MusicParameters', () => {

    test('renders MusicParameters without crashing', () => {
        render(
            <MusicParameters detectedEmotion=""
                             musicParameter1=""
                             musicParameter2=""
                             musicParameter3={['']}/>
        );
    });
    test('handles popularity change', () => {
        const {getByTestId} = render(<MusicParameters detectedEmotion=""
                                                      musicParameter1=""
                                                      musicParameter2=""
                                                      musicParameter3={['']}/>);
        const select = getByTestId('popularity-select');

        fireEvent.change(select, {target: {selectOptions: 'mainstream'}});

        expect(select.selectOptions).toBe('mainstream');
    });
    test('handles personalization change', () => {
        const {getByTestId} = render(<MusicParameters detectedEmotion=""
                                                      musicParameter1=""
                                                      musicParameter2=""
                                                      musicParameter3={['']}/>);
        const select = getByTestId('personalization-select');

        fireEvent.change(select, {target: {selectOptions: 'high'}});
        expect(select.selectOptions).toBe('high');
    });
    test('handles genres change', () => {
        const {getByTestId} = render(<MusicParameters detectedEmotion=""
                                                      musicParameter1=""
                                                      musicParameter2=""
                                                      musicParameter3={['']}/>);
        const select = getByTestId('genres-select');
        fireEvent.change(select, {target: {selectOptions: ['pop', 'rock']}});
        expect(select.selectOptions).toStrictEqual(['pop', 'rock']);
    });
    test('button is disabled when parameters are not selected', () => {
        const {getByText} = render(<MusicParameters detectedEmotion=""
                                                    musicParameter1=""
                                                    musicParameter2=""
                                                    musicParameter3={['']}/>);
        const button = getByText('Recommend music');
        expect(button).toBeDisabled();
    });
        test('button is disabled when not all parameters are not selected', () => {
        const {getByText} = render(<MusicParameters detectedEmotion="happy"
                                                    musicParameter1=""
                                                    musicParameter2="high"
                                                    musicParameter3={['']}/>);
        const button = getByText('Recommend music');
        expect(button).toBeDisabled();
    });
    test('button is enabled when parameters are selected', () => {
        const {getByText} = render(<MusicParameters detectedEmotion="happy"
                                                    musicParameter1="mainstream"
                                                    musicParameter2="high"
                                                    musicParameter3={['pop']}
        />);
        const button = getByText('Recommend music');


        expect(button).toBeEnabled();
    });
    test('fetches playlist on button click', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({data: []}),
            })
        );
        const {getByText} = render(<MusicParameters detectedEmotion="happy"
                                                    musicParameter1="mainstream"
                                                    musicParameter2="high"
                                                    musicParameter3={['pop']}
                                                    handlePlaylistRecommendation={jest.fn().mockResolvedValue({})}
        />);
        const button = getByText('Recommend music');
        fireEvent.click(button);
        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledWith(
                'http://127.0.0.1:8000/create-playlist-based-on-parameters',
                expect.objectContaining({
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        "emotion": "happy", // Update with your expected values
                        "personalization": "high",
                        "popularity": "mainstream",
                        "genres": ['pop'],
                    }),
                })
            );
        });
    });
    test('handles errors during playlist fetch:', async () => {
        const logSpy = jest.spyOn(console, 'log');
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: false,
                json: async () => ({error: 'Test error message'}),
                status: 500,
            })
        );
        const {getByText} = render(<MusicParameters detectedEmotion="happy"
                                                    musicParameter1="mainstream"
                                                    musicParameter2="high"
                                                    musicParameter3={['pop']}
                                                    handlePlaylistRecommendation={jest.fn().mockResolvedValue({})}
        />);
        const button = getByText('Recommend music');
        fireEvent.click(button);
        await waitFor(() => {
            expect(logSpy).toHaveBeenCalledWith(
                expect.stringContaining("Error when trying to get recommended playlist:")
            );
        });
    });
    test('update setPlaylistSongURI when playlist fetch', async () => {
        const props = {
            detectedEmotion: 'happy',
            musicParameter1: 'mainstream',
            musicParameter2: 'high',
            musicParameter3: ['pop'],
            handlePlaylistRecommendation: jest.fn(),
            setRecommendedPlaylist: jest.fn(),
            setPlaylistSongURI: jest.fn(),
            setIsPlaylistEmpty: jest.fn(),
            setPlaylistChangeGuard: jest.fn(),
        };
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({data: [{uri: 'song1'}, {uri: 'song2'}]}),
            })
        );
        const {getByText} = render(<MusicParameters {...props}
        />);
        const button = getByText('Recommend music');
        fireEvent.click(button);
        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledWith(
                'http://127.0.0.1:8000/create-playlist-based-on-parameters',
                expect.objectContaining({
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        "emotion": "happy", // Update with your expected values
                        "personalization": "high",
                        "popularity": "mainstream",
                        "genres": ['pop'],
                    }),
                })
            );
            expect(props.setPlaylistSongURI).toHaveBeenCalledWith(
                expect.arrayContaining(['song1', 'song2'])
            );
        });
    });
});
