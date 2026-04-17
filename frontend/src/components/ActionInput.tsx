import { useState, type KeyboardEvent } from 'react';

interface Props {
  onSubmit: (action: string) => void;
  disabled: boolean;
}

export function ActionInput({ onSubmit, disabled }: Props) {
  const [value, setValue] = useState('');

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSubmit(trimmed);
    setValue('');
  };

  const handleKey = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') submit();
  };

  return (
    <div style={styles.container}>
      <span style={styles.prompt}>&gt;</span>
      <input
        style={styles.input}
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKey}
        disabled={disabled}
        placeholder={disabled ? 'Thinking...' : 'What do you do?'}
        autoFocus
        autoComplete="off"
        spellCheck={false}
      />
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    alignItems: 'center',
    borderTop: '1px solid #3a3020',
    paddingTop: '0.75rem',
    marginTop: '0.5rem',
    gap: '0.5rem',
  },
  prompt: {
    color: '#6a8a6a',
    fontSize: '1rem',
    flexShrink: 0,
  },
  input: {
    flex: 1,
    background: 'transparent',
    border: 'none',
    outline: 'none',
    color: '#d4c080',
    fontFamily: 'inherit',
    fontSize: '0.95rem',
  },
};
