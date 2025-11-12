# Frontend - Stock Streaming UI

React TypeScript application for visualizing real-time stock data.

## Features

- ✅ Real-time WebSocket connection to backend
- ✅ Live stock price updates with animations
- ✅ Bid/Ask spreads and sizes
- ✅ Connection status indicator
- ✅ Automatic reconnection with exponential backoff
- ✅ Responsive design for all screen sizes
- ✅ Modern dark theme UI

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **WebSocket API** - Real-time communication
- **CSS3** - Styling with animations

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── StockCard.tsx           # Individual stock display
│   │   ├── StockCard.css
│   │   ├── ConnectionStatus.tsx    # WebSocket status indicator
│   │   └── ConnectionStatus.css
│   ├── hooks/
│   │   └── useWebSocket.ts         # Custom WebSocket hook
│   ├── types/
│   │   └── index.ts                # TypeScript type definitions
│   ├── App.tsx                     # Main application
│   ├── App.css
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Components

### App.tsx
Main application component that:
- Manages WebSocket connection
- Stores stock data state
- Fetches initial quotes
- Renders stock cards

### StockCard.tsx
Displays individual stock information:
- Current price with change indicator
- Bid/Ask prices and sizes
- Trade information
- Animated price changes
- Timestamp of last update

### ConnectionStatus.tsx
Shows WebSocket connection status:
- 🟢 Connected
- 🟡 Connecting...
- 🔴 Disconnected
- ❌ Error

## Custom Hooks

### useWebSocket
Manages WebSocket connection with:
- Automatic reconnection
- Exponential backoff (up to 30 seconds)
- Connection state management
- Message sending/receiving
- Cleanup on unmount

**Usage:**
```typescript
const { connectionStatus, sendMessage } = useWebSocket(
  'ws://localhost:8000/ws',
  (data) => {
    // Handle incoming messages
    console.log('Received:', data)
  }
)
```

## Type Definitions

### StockData
```typescript
interface StockData {
  symbol: string
  type?: 'quote' | 'trade'
  bid?: number
  ask?: number
  bidSize?: number
  askSize?: number
  price?: number
  size?: number
  timestamp?: string
  lastUpdate: number
  error?: string
}
```

### ConnectionStatus
```typescript
type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error'
```

## Styling

### CSS Variables
Customize colors in `src/index.css`:

```css
:root {
  --bg-primary: #0f172a;      /* Main background */
  --bg-secondary: #1e293b;    /* Card background */
  --bg-tertiary: #334155;     /* Detail background */
  --text-primary: #f8fafc;    /* Main text */
  --text-secondary: #cbd5e1;  /* Secondary text */
  --accent-green: #10b981;    /* Positive/Bid */
  --accent-red: #ef4444;      /* Negative/Ask */
  --accent-blue: #3b82f6;     /* Highlights */
  --border-color: #475569;    /* Borders */
}
```

### Animations

**Price Change Animations:**
- `priceUp` - Green flash on price increase
- `priceDown` - Red flash on price decrease

**Price Indicators:**
- ↗ Green arrow for increases
- ↘ Red arrow for decreases

**Connection Status:**
- Pulsing animation while connecting

## Development

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```

Opens at `http://localhost:3000` with hot reload.

### Build for Production
```bash
npm run build
```

Creates optimized build in `dist/` directory.

### Preview Production Build
```bash
npm run preview
```

### Lint Code
```bash
npm run lint
```

## Configuration

### WebSocket URL

Edit in `src/App.tsx`:
```typescript
const { connectionStatus, sendMessage } = useWebSocket(
  'ws://localhost:8000/ws',  // Change for production
  (data) => { ... }
)
```

### API Base URL

Edit in `src/App.tsx`:
```typescript
fetch('http://localhost:8000/api/quotes')  // Change for production
```

### Tracked Symbols

Edit in `src/App.tsx`:
```typescript
const SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
```

### Vite Configuration

Edit `vite.config.ts`:
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,  // Development port
    open: true,  // Auto-open browser
  },
})
```

## Responsive Design

Breakpoints:
- **Desktop:** > 768px (Grid layout)
- **Mobile:** ≤ 768px (Single column)

Grid automatically adjusts based on screen size:
```css
.stock-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}
```

## Performance Optimizations

- React.StrictMode for development checks
- Efficient state updates with functional updates
- Debounced animations to prevent excessive re-renders
- WebSocket message throttling
- Cleanup effects to prevent memory leaks

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

Requires:
- WebSocket API support
- CSS Grid support
- CSS Custom Properties support

## Deployment

### Build
```bash
npm run build
```

### Deploy to Vercel
```bash
npm i -g vercel
vercel
```

### Deploy to Netlify
```bash
npm i -g netlify-cli
netlify deploy --prod --dir=dist
```

### Environment Variables

For production, set:
- `VITE_WS_URL` - WebSocket endpoint
- `VITE_API_URL` - REST API endpoint

Access in code:
```typescript
const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
```

## Troubleshooting

### WebSocket won't connect
1. Ensure backend is running
2. Check WebSocket URL
3. Look for CORS errors in console
4. Verify network/firewall settings

### No data showing
1. Check browser console for errors
2. Verify backend is receiving data from Alpaca
3. Check market hours
4. Inspect WebSocket messages in DevTools

### Styles not applying
1. Check browser developer tools
2. Verify CSS files are imported
3. Clear browser cache
4. Check for CSS specificity issues

## Development Tips

### React Developer Tools
Install [React DevTools](https://react.dev/learn/react-developer-tools) for debugging.

### Network Debugging
Use browser DevTools > Network > WS to inspect WebSocket messages.

### TypeScript Strict Mode
All type checking is enabled. Fix TypeScript errors before building.

## License

MIT

