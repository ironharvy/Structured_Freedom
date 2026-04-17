import { useState, useEffect, useCallback } from 'react';
import { createSession, executeTurn } from './api/client';
import { LocationPanel } from './components/LocationPanel';
import { GameLog } from './components/GameLog';
import { InventoryPanel } from './components/InventoryPanel';
import { QuestPanel } from './components/QuestPanel';
import { ActionInput } from './components/ActionInput';
import type { StateSnapshot, LogEntry } from './types/game';

let logCounter = 0;

export default function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [state, setState] = useState<StateSnapshot | null>(null);
  const [log, setLog] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    createSession('Traveller')
      .then((res) => {
        setSessionId(res.session_id);
        setState(res.state);
        setLog([{
          id: ++logCounter,
          input: '',
          narration: `Welcome to Ashford. ${res.state.location_description}`,
          success: true,
        }]);
      })
      .catch((e) => setError(String(e)));
  }, []);

  const handleAction = useCallback(async (action: string) => {
    if (!sessionId || loading) return;
    setLoading(true);
    try {
      const res = await executeTurn(sessionId, action);
      setState(res.state);
      setLog((prev) => [
        ...prev,
        { id: ++logCounter, input: action, narration: res.narration, success: res.success },
      ]);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }, [sessionId, loading]);

  if (error) {
    return (
      <div style={styles.error}>
        <div>Error: {error}</div>
        <div style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#806060' }}>
          Make sure the backend is running on port 8000.
        </div>
      </div>
    );
  }

  if (!state) {
    return <div style={styles.loading}>Loading world…</div>;
  }

  return (
    <div style={styles.layout}>
      <div style={styles.main}>
        <LocationPanel state={state} />
        <GameLog entries={log} loading={loading} />
        <ActionInput onSubmit={handleAction} disabled={loading} />
      </div>
      <div style={styles.sidebar}>
        <InventoryPanel inventory={state.inventory} />
        <QuestPanel quests={state.quests} />
        <div style={styles.turnCounter}>Turn {state.turn_number}</div>
      </div>
    </div>
  );
}

const styles = {
  layout: {
    display: 'flex',
    height: '100vh',
    maxWidth: '1100px',
    margin: '0 auto',
    padding: '1.5rem',
    gap: '1.5rem',
  },
  main: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column' as const,
    minWidth: 0,
  },
  sidebar: {
    width: '220px',
    flexShrink: 0,
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.5rem',
  },
  error: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    color: '#c05050',
    fontFamily: 'Courier New, monospace',
  },
  loading: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    color: '#7a6a50',
    fontFamily: 'Courier New, monospace',
  },
  turnCounter: {
    color: '#4a4030',
    fontSize: '0.75rem',
    textAlign: 'right' as const,
    marginTop: 'auto',
  },
};
