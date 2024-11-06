import React, { createContext, useContext, useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { themes } from '../themes/themes';

type ThemeContextType = {
  theme: string;
  mode: 'light' | 'dark';
  setTheme: (theme: string) => void;
  toggleMode: () => void;
};

const ThemeContext = createContext<ThemeContextType>({} as ThemeContextType);

export const ThemeContextProvider = ({ children }: { children: React.ReactNode }) => {
  const [theme, setTheme] = useState('matrix');
  const [mode, setMode] = useState<'light' | 'dark'>('dark');

  const toggleMode = () => setMode(mode === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, mode, setTheme, toggleMode }}>
      <ThemeProvider theme={themes[theme][mode]}>
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
