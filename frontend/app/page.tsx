import TextToSpeechForm from './components/TextToSpeechForm';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-50">
      <div className="w-full max-w-4xl">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-900">
          Text to Speech Converter
        </h1>
        <TextToSpeechForm />
      </div>
    </main>
  );
}
