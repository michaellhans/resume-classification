import { Helmet } from 'react-helmet-async';
import { Link as RouterLink } from 'react-router-dom';
// @mui
import { styled } from '@mui/material/styles';
import { Link, Container, Typography, Divider, Stack, Button } from '@mui/material';
// hooks
import useResponsive from '../hooks/useResponsive';
// components
import Logo from '../components/logo';
import Iconify from '../components/iconify';
// sections

// ----------------------------------------------------------------------

const StyledRoot = styled('div')(({ theme }) => ({
  [theme.breakpoints.up('md')]: {
    display: 'flex',
  },
}));

const StyledSection = styled('div')(({ theme }) => ({
  width: '100%',
  maxWidth: 480,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  boxShadow: theme.customShadows.card,
  backgroundColor: theme.palette.background.default,
}));

const StyledContent = styled('div')(({ theme }) => ({
  maxWidth: 480,
  margin: 'auto',
  minHeight: '100vh',
  display: 'flex',
  justifyContent: 'center',
  flexDirection: 'column',
  padding: theme.spacing(12, 0),
}));

// ----------------------------------------------------------------------

export default function HomePage() {
  const mdUp = useResponsive('up', 'md');

  return (
    <>
      <Helmet>
        <title> Login | Minimal UI </title>
      </Helmet>

      <StyledRoot>
        <Logo
          sx={{
            position: 'fixed',
            top: { xs: 16, sm: 24, md: 40 },
            left: { xs: 16, sm: 24, md: 40 },
          }}
        />

        {mdUp && (
          <StyledSection>
            <Typography variant="h3" sx={{ px: 5, mt: 10, mb: 5 }}>
              Hi, Welcome Back
            </Typography>
            <img src="/assets/illustrations/cv3.jpg" alt="home" />
          </StyledSection>
        )}

        <Container maxWidth="sm">
          <StyledContent>
            <Typography variant="h4" gutterBottom>
            Get Job Position Predictions with Magic Tool
            </Typography>
            <Typography variant="body2" sx={{ mb: 5 }}>
              Click "Upload" for Get Job Prediction {''}
              <Link variant="subtitle2">   Get started</Link>
            </Typography>
            <Button variant="contained" size="large" component="label">
            Upload
            <input hidden accept="file/*" multiple type="file"/>
          </Button>
          <Divider sx={{ my: 3 }}>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                OR
              </Typography>
            </Divider>
            <Stack direction="row" spacing={2}>
              
              <Button to="https://drive.google.com" fullWidth size="large" color="inherit" variant="outlined" component={RouterLink}>
                <Iconify icon="logos:google-drive" color="#1FA463" width={22} height={22} />
              </Button>
              

              <Button to="https://www.dropbox.com" fullWidth size="large" color="inherit" variant="outlined" component={RouterLink}>
                <Iconify icon="logos:dropbox" color="#0060ff" width={22} height={22} />
              </Button>

              <Button Button to="https://onedrive.live.com" fullWidth size="large" color="inherit" variant="outlined" component={RouterLink}>
                <Iconify icon="logos:microsoft-onedrive" color="#1C9CEA" width={22} height={22} />
              </Button>
            </Stack>
            <Divider sx={{ my: 3 }}>
              <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                SUBMIT
              </Typography>
            </Divider>
            <Button to="/result" variant="contained" color="warning" size="large" component={RouterLink}>
            Submit
          </Button>
          </StyledContent>
        </Container>
      </StyledRoot>
    </>
  );
}
