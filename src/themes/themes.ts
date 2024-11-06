import { createTheme } from '@mui/material/styles';

export const matrixTheme = {
  dark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#00ff00' },
      background: { default: '#000000', paper: '#001100' },
      text: { primary: '#00ff00', secondary: '#00dd00' }
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: `
          @keyframes scanline {
            0% { transform: translateY(0); }
            100% { transform: translateY(100%); }
          }
          body::after {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100px;
            background: linear-gradient(transparent, #00ff0015, transparent);
            animation: scanline 8s linear infinite;
            pointer-events: none;
          }
        `
      }
    }
  }),
  light: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#006600' },
      background: { default: '#f0fff0', paper: '#ffffff' },
      text: { primary: '#003300', secondary: '#006600' }
    }
  })
};

export const cgaTheme = {
  dark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#55ffff' },
      secondary: { main: '#ff55ff' },
      background: { default: '#000000', paper: '#000055' },
      text: { primary: '#ffffff', secondary: '#55ffff' }
    },
    typography: {
      fontFamily: "'DOS', 'Courier New', monospace"
    }
  }),
  light: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#0000aa' },
      secondary: { main: '#aa00aa' },
      background: { default: '#ffffff', paper: '#aaaaff' },
      text: { primary: '#000000', secondary: '#0000aa' }
    },
    typography: {
      fontFamily: "'DOS', 'Courier New', monospace"
    }
  })
};

export const synthwaveTheme = {
  dark: createTheme({
    palette: {
      mode: 'dark',
      primary: { main: '#ff00ff' },
      secondary: { main: '#00ffff' },
      background: { default: '#1a0b2e', paper: '#2d1b4e' },
      text: { primary: '#ff00ff', secondary: '#00ffff' }
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: `
          body {
            background: linear-gradient(#1a0b2e, #2d1b4e);
            background-size: 100% 100vh;
          }
        `
      }
    }
  }),
  light: createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#ff1b8d' },
      secondary: { main: '#1bffff' },
      background: { default: '#f0e6ff', paper: '#ffffff' },
      text: { primary: '#2d1b4e', secondary: '#ff1b8d' }
    }
  })
};

export const themes = {
  matrix: matrixTheme,
  cga: cgaTheme,
  synthwave: synthwaveTheme
};
