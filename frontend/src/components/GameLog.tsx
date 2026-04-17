import { useEffect, useRef } from 'react';
import type { LogEntry } from '../types/game';

interface Props {
  entries: LogEntry[];
  loading: boolean;
}

export function GameLog({ entries, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [entries, loading]);

  return (
    <div style={styles.container}>
      {entries.map((e) => (
        <div key={e.id} style={styles.entry}>
          <span style={styles.prompt}>&gt; </span>
          <span style={styles.input}>{e.input}</span>
          <div style={{ ...styles.narration, color: e.success ? '#c9b99a' : '#a05050' }}>
            {e.narration}
          </div>
        </div>
      ))}
      {loading && (
        <div style={styles.thinking}>
          <span style={styles.prompt}>&gt; </span>
          <span style={styles.blink}>▋</span>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}

const styles = {
  container: {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '0.5rem 0',
    minHeight: 0,
  },
  entry: {
    marginBottom: '1rem',
  },
  prompt: {
    color: '#6a8a6a',
  },
  input: {
    color: '#d4c080',
  },
  narration: {
    marginTop: '0.3rem',
    paddingLeft: '1.2rem',
    lineHeight: '1.7',
  },
  thinking: {
    color: '#6a8a6a',
  },
  blink: {
    animation: 'blink 1s step-start infinite',
  },
};
