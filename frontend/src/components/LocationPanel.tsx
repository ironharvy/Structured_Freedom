import type { StateSnapshot } from '../types/game';

interface Props {
  state: StateSnapshot;
}

export function LocationPanel({ state }: Props) {
  return (
    <div style={styles.container}>
      <div style={styles.name}>{state.location_name}</div>
      <div style={styles.description}>{state.location_description}</div>
    </div>
  );
}

const styles = {
  container: {
    borderBottom: '1px solid #3a3020',
    paddingBottom: '0.75rem',
    marginBottom: '0.75rem',
  },
  name: {
    color: '#e8c87a',
    fontWeight: 'bold',
    fontSize: '1.05rem',
    marginBottom: '0.3rem',
    textTransform: 'uppercase' as const,
    letterSpacing: '0.05em',
  },
  description: {
    color: '#a89070',
    fontStyle: 'italic' as const,
  },
};
