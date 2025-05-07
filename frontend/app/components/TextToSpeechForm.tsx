'use client'

import { useState } from 'react';
import { convertTextToSpeech, TextToSpeechResponse } from '../services/api';

export default function TextToSpeechForm() {
  const [text, setText] = useState('');
  const [speed, setSpeed] = useState<number>(22050); // Default speed
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter some text to convert');
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      const response = await convertTextToSpeech(text, speed);
      console.log("convertTextToSpeech--->", response);
      setAudioUrl(response.audio_url);
    } catch (err) {
      setError('Failed to convert text to speech. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-slate-50 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Text to Speech Converter</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-1">
            Enter text to convert to speech
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full px-3 py-2 border text-gray-950 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            rows={6}
            placeholder="Type your text here..."
          />
        </div>
        
        <div>
          <label htmlFor="speed" className="block text-sm font-medium text-gray-700 mb-1">
            Speech Speed (Sample Rate): {speed} Hz
          </label>
          <input
            id="speed"
            type="range"
            min="11025"
            max="44100"
            step="50"
            value={speed}
            onChange={(e) => setSpeed(Math.round(Number(e.target.value)))}
            className="w-full"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Slower (11025 Hz)</span>
            <span>Default (22050 Hz)</span>
            <span>Faster (44100 Hz)</span>
          </div>
        </div>
        
        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Converting...' : 'Convert to Speech'}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 text-red-600 text-sm">
          {error}
        </div>
      )}
      
      {audioUrl && (
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-800 mb-2">Generated Speech</h3>
          <audio controls className="w-full" src={audioUrl}>
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
} 