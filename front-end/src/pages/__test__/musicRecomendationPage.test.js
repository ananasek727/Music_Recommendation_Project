import React from 'react';
import {render, screen, fireEvent, act} from '@testing-library/react';
import MusicRecommendationPage from '../MusicRecommendation';

describe('MusicRecommendationPage component', () => {
    test('renders without crashing', () => {
        render(<MusicRecommendationPage/>);
    });

    test('Web cam button works', () => {
        render(<MusicRecommendationPage/>);
        const webcamButton = screen.getByText(/Web cam/i);
        fireEvent.click(webcamButton);
        expect(screen.getByText("Take photo")).toBeInTheDocument();


    })
    test('Upload image button works', () => {
        render(<MusicRecommendationPage/>);
        const uploadButton = screen.getByText(/Upload image/i);
        fireEvent.click(uploadButton);
        expect(screen.getByTestId("input-file")).toBeInTheDocument();

    })
    test('allows switching between webcam and image upload', () => {
        render(<MusicRecommendationPage/>);
        const webcamButton = screen.getByText(/Web cam/i);
        fireEvent.click(webcamButton);
        expect(screen.getByText("Take photo")).toBeInTheDocument();
        const backButton = screen.getByText("Back");
        fireEvent.click(backButton)
        const uploadButton = screen.getByText(/Upload image/i);
        fireEvent.click(uploadButton);
        expect(screen.getByTestId("input-file")).toBeInTheDocument();
    });
    test('display music parameters', () => {
        render(<MusicRecommendationPage/>)
        expect(screen.getByText('Recommend music')).toBeInTheDocument()
    });
    test('display music control', () => {
        render(<MusicRecommendationPage/>)
        expect(screen.getByText('Next track')).toBeInTheDocument()
    });

});
