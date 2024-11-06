import React from 'react';
import { Box, Card, FormControl, InputLabel, MenuItem, Select, Stack, Typography, IconButton } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useTheme } from '../contexts/ThemeContext';

export const ThemeSelector = () => {
  const { theme, mode, setTheme, toggleMode } = useTheme();

  return (
    <Card sx={{ p: 2, m: 2 }}>
      <Typography variant="h6" gutterBottom>Theme Settings</Typography>
      <Stack spacing={2}>
        <FormControl fullWidth>
          <InputLabel>Theme</InputLabel>
          <Select
            value={theme}
            label="Theme"
            onChange={(e) => setTheme(e.target.value)}
          >
            <MenuItem value="matrix">Matrix Terminal</MenuItem>
            <MenuItem value="cga">CGA DOS</MenuItem>
            <MenuItem value="synthwave">Synthwave</MenuItem>
          </Select>
        </FormControl>
        
        <Box display="flex" alignItems="center" gap={1}>
          <Typography>Mode:</Typography>
          <IconButton onClick={toggleMode}>
            {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
            {mode === 'dark' ? ' Light Mode' : ' Dark Mode'}
          </IconButton>
        </Box>
      </Stack>
    </Card>
  );
};
