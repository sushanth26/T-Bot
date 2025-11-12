import { ConnectionStatus as Status } from '../types'
import './ConnectionStatus.css'

interface ConnectionStatusProps {
  status: Status
}

const ConnectionStatus = ({ status }: ConnectionStatusProps) => {
  const getStatusInfo = () => {
    switch (status) {
      case 'connected':
        return { text: 'Connected', className: 'connected', icon: '🟢' }
      case 'connecting':
        return { text: 'Connecting...', className: 'connecting', icon: '🟡' }
      case 'disconnected':
        return { text: 'Disconnected', className: 'disconnected', icon: '🔴' }
      case 'error':
        return { text: 'Error', className: 'error', icon: '❌' }
    }
  }

  const statusInfo = getStatusInfo()

  return (
    <div className={`connection-status ${statusInfo.className}`}>
      <span className="status-icon">{statusInfo.icon}</span>
      <span className="status-text">{statusInfo.text}</span>
    </div>
  )
}

export default ConnectionStatus

