interface Props {
  inventory: string[];
}

export function InventoryPanel({ inventory }: Props) {
  return (
    <div style={styles.container}>
      <div style={styles.title}>Inventory</div>
      {inventory.length === 0 ? (
        <div style={styles.empty}>Nothing carried.</div>
      ) : (
        <ul style={styles.list}>
          {inventory.map((item) => (
            <li key={item} style={styles.item}>{item}</li>
          ))}
        </ul>
      )}
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
  empty: {
    color: '#5a5040',
    fontStyle: 'italic' as const,
    fontSize: '0.85rem',
  },
  list: {
    listStyle: 'none',
    padding: 0,
  },
  item: {
    color: '#b0a880',
    fontSize: '0.85rem',
    padding: '0.1rem 0',
  },
};
