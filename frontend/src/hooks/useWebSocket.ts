import { useState, useEffect, useCallback, useRef } from 'react'
import { ConnectionStatus } from '../types'

export const useSSE = (
  url: string,
  onMessage: (data: any) => void
) => {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('connecting')
  const eventSourceRef = useRef<EventSource | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>()
  const reconnectAttemptsRef = useRef(0)

  const connect = useCallback(() => {
    try {
      const eventSource = new EventSource(url)
      eventSourceRef.current = eventSource

      eventSource.onopen = () => {
        console.log('SSE connected')
        setConnectionStatus('connected')
        reconnectAttemptsRef.current = 0
      }

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          onMessage(data)
        } catch (error) {
          console.error('Failed to parse SSE message:', error)
        }
      }

      eventSource.onerror = (error) => {
        console.error('SSE error:', error)
        setConnectionStatus('error')
        eventSource.close()
        eventSourceRef.current = null

        // Attempt to reconnect with exponential backoff
        const maxAttempts = 10
        if (reconnectAttemptsRef.current < maxAttempts) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000)
          console.log(`Reconnecting in ${delay}ms... (attempt ${reconnectAttemptsRef.current + 1}/${maxAttempts})`)
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttemptsRef.current += 1
            setConnectionStatus('connecting')
            connect()
          }, delay)
        }
      }
    } catch (error) {
      console.error('Failed to create SSE connection:', error)
      setConnectionStatus('error')
    }
  }, [url, onMessage])

  useEffect(() => {
    connect()

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (eventSourceRef.current) {
        eventSourceRef.current.close()
      }
    }
  }, [connect])

  return { connectionStatus }
}

