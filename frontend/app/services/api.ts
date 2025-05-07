// API service for text-to-speech conversion
export interface TextToSpeechResponse {
  audio_url: string;
}

export interface TextToSpeechRequest {
  text: string;
  speed: number;
}

export const convertTextToSpeech = async (text: string, speed: number = 22050): Promise<TextToSpeechResponse> => {
  try {
    const response = await fetch('http://localhost:8000/api/convert-to-speech', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, speed }),
    });

    if (!response.ok) {
      throw new Error('Failed to convert text to speech');
    }

    return await response.json();
  } catch (error) {
    console.error('Error converting text to speech:', error);
    throw error;
  }
}; 