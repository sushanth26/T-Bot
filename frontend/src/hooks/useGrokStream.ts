import { useState, useEffect, useRef } from 'react';
import { GrokAnalysis } from '../types';

interface UseGrokStreamResult {
  analysis: GrokAnalysis | null;
  streamingText: string;
  isStreaming: boolean;
  error: string | null;
}

export function useGrokStream(symbol: string | null): UseGrokStreamResult {
  const [analysis, setAnalysis] = useState<GrokAnalysis | null>(null);
  const [streamingText, setStreamingText] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!symbol) {
      setAnalysis(null);
      setStreamingText('');
      setIsStreaming(false);
      return;
    }

    // Clean up any existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    // Reset states
    setAnalysis(null);
    setStreamingText('');
    setIsStreaming(true);
    setError(null);

    // Create new EventSource for streaming
    const eventSource = new EventSource(`http://localhost:8000/api/grok/stream/${symbol}`);
    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.error) {
          setError(data.error);
          setIsStreaming(false);
          eventSource.close();
          return;
        }

        if (data.type === 'content') {
          // Append streaming content
          setStreamingText((prev) => prev + data.chunk);
        } else if (data.type === 'complete') {
          // Analysis complete, parse and set final result
          setAnalysis(data.analysis);
          setIsStreaming(false);
          setStreamingText('');
          eventSource.close();
        }
      } catch (err) {
        console.error('Error parsing SSE data:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('EventSource error:', err);
      setError('Connection error');
      setIsStreaming(false);
      eventSource.close();
    };

    // Cleanup on unmount or symbol change
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [symbol]);

  return { analysis, streamingText, isStreaming, error };
}

