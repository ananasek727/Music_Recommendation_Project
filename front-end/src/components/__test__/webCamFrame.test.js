import WebCamFrame from "../WebCamFrame";
import * as React from 'react';
import {render, fireEvent, waitFor, screen} from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import {act} from "react-dom/test-utils";

describe('WebCamFrame Component Tests', () => {
    test('Renders without crashing', () => {
        render(<WebCamFrame/>);
    });

    test('Clicking the back button calls setImgDecision', () => {
        const setImgDecisionMock = jest.fn();
        render(<WebCamFrame setImgDecision={setImgDecisionMock}/>);
        fireEvent.click(screen.getByText('Back'));
        expect(setImgDecisionMock).toHaveBeenCalledWith(0);
    });

    test('Clicking the take photo button calls capture function', () => {
        const getScreenshotMock = jest.fn();
        const webcamRefMock = { current: { getScreenshot: getScreenshotMock } };
        const setImgSrcMock = jest.fn();
        render(<WebCamFrame capture={webcamRefMock} setImgSrc={setImgSrcMock}/>);
        const button = screen.getByText('Take photo')
        fireEvent.click(button);
        expect(setImgSrcMock).toHaveBeenCalled();
  });

    test('Clicking the retake photo button calls retake function', () => {
        const retakeMock = jest.fn();
        const setImgSrcMock = jest.fn();
        render(<WebCamFrame retake={retakeMock} setImgSrc={setImgSrcMock} imgSrc="someBase64Image"/>);
        fireEvent.click(screen.getByText('Retake photo'));
        expect(setImgSrcMock).toHaveBeenCalled();
    });

    test('Renders webcam when there is no image source', () => {
        render(<WebCamFrame imgSrc={false}/>);
        expect(screen.getAllByTestId("webcam-component")[0]).toBeInTheDocument();
    });

    test('Renders captured image', () => {
        render(<WebCamFrame imgSrc="img-url"/>);
        expect(screen.getByRole('img')).toBeInTheDocument();
    });

    test('Calls handleEmotionPrediction works',  async() => {
    const logSpy = jest.spyOn(console, 'log');
    const mockJson = jest.fn().mockResolvedValue({ emotion: 'happy' });
    const mockResponse = { ok: true, json: mockJson };
    global.fetch = jest.fn().mockResolvedValue(mockResponse);
    const props = {
      imgSrc: 'yourBase64String',
      setDetectedEmotion: jest.fn(),
    };

    render(<WebCamFrame {...props} />);
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/get-emotion-from-photo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ base64_photo: 'yourBase64String' }),
    });
        await waitFor(() => {
            expect(logSpy).toHaveBeenCalledWith(
                expect.objectContaining({ emotion: 'happy' })
            );
        });
    });

    test('Displays detected emotion when available', () => {
        render(<WebCamFrame detectedEmotion="Happy"/>);
        expect(screen.getByText('Happy')).toBeInTheDocument();
    });

    test('Retake function sets imgSrc to null', () => {
        const setImgSpy = jest.fn();
        const retakeSpy = jest.fn();
        render(<WebCamFrame retake={retakeSpy} imgSrc="someBase64Image" setImgSrc={setImgSpy}/>);
        fireEvent.click(screen.getByText('Retake photo'));
        expect(setImgSpy).toHaveBeenCalledWith(null);
    });

});
