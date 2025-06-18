import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { QrCodeScanner } from '@mui/icons-material';

const Header = () => {
  return (
    <AppBar position="static" elevation={1}>
      <Toolbar>
        <QrCodeScanner sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          バーコードスキャナー
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="body2" color="inherit">
            v1.0.0
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 