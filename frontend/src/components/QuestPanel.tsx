import type { QuestInfo } from '../types/game';

interface Props {
  quests: Record<string, QuestInfo>;
}

export function QuestPanel({ quests }: Props) {
  const entries = Object.entries(quests);
  if (entries.length === 0) return null;

  return (
    <div style={styles.container}>
      <div style={styles.title}>Objectives</div>
      {entries.map(([id, q]) => (
        <div key={id} style={styles.quest}>
          {q.active.map((obj) => (
            <div key={obj} style={styles.active}>◇ {obj}</div>
          ))}
          {q.completed.map((obj) => (
            <div key={obj} style={styles.completed}>◆ {obj}</div>
          ))}
        </div>
      ))}
    </div>
  );
}

const styles = {
  container: {
    borderTop: '1px solid #3a3020',
    paddingTop: '0.75rem',
    marginTop: '0.5rem',
  },
  title: {
    color: '#e8c87a',
    fontWeight: 'bold' as const,
    textTransform: 'uppercase' as const,
    letterSpacing: '0.05em',
    marginBottom: '0.4rem',
    fontSize: '0.85rem',
  },
  quest: {
    marginBottom: '0.3rem',
  },
  active: {
    color: '#90b090',
    fontSize: '0.82rem',
    padding: '0.1rem 0',
  },
  completed: {
    color: '#505848',
    textDecoration: 'line-through' as const,
    fontSize: '0.82rem',
    padding: '0.1rem 0',
  },
};
