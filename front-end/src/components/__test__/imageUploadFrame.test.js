import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import ImageUploadFrame from '../ImageUploadFrame';
import userEvent from "@testing-library/user-event";
describe('ImageUploadFrame', () => {
  it('renders without crashing', () => {
    render(<ImageUploadFrame />);
    expect(screen.getByText('Back')).toBeInTheDocument();
  });

  it('handles emotion prediction correctly', async () => {
    const setDetectedEmotion = jest.fn();
    const setImgSrc = jest.fn();
    render(<ImageUploadFrame setDetectedEmotion={setDetectedEmotion} setImgSrc={setImgSrc} imgSrc="test" />);

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ emotion: 'happy' }),
    });

    await act(async () => {
      fireEvent.click(screen.getByText('Predict emotion'));
    });
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/get-emotion-from-photo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ base64_photo: 'test' }),
    });
    expect(setDetectedEmotion).toHaveBeenCalledWith('happy');
  });


  it('resets image source when "Reupload image" button is clicked', async () => {
    const setImgSrc = jest.fn();
    render(<ImageUploadFrame setImgSrc={setImgSrc} imgSrc="dummyBase64" />);
    await act(async () => {
      fireEvent.click(screen.getByText('Reupload image'));
    });
    expect(setImgSrc).toHaveBeenCalledWith(null);
  });

  it('renders the detected emotion when available', () => {
    const detectedEmotion = 'happy';
    const { getByText } = render(<ImageUploadFrame detectedEmotion={detectedEmotion} />);

    expect(getByText(detectedEmotion)).toBeInTheDocument();
  });

  it('calls the provided callback when the "Back" button is clicked', () => {
    const setImgDecision = jest.fn();
    const { getByText } = render(<ImageUploadFrame setImgDecision={setImgDecision} />);

    fireEvent.click(getByText('Back'));

    expect(setImgDecision).toHaveBeenCalledWith(0);
  });
});
