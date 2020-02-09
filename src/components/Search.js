import React from 'react';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import CircularProgress from '@material-ui/core/CircularProgress';
import {InputBase} from "@material-ui/core";
import {fade, makeStyles} from "@material-ui/core/styles";
import Network from "../classes/Network";

function sleep(delay = 0) {
  return new Promise(resolve => {
    setTimeout(resolve, delay);
  });
}

const useStyles = makeStyles(theme => ({
  inputRoot: {
    color: 'inherit',
  },
  inputInput: {
    padding: theme.spacing(1, 1, 1, 7),
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      width: 120,
      '&:focus': {
        width: 200,
      },
    },
  },
}));

export default function Search() {
  const [open, setOpen] = React.useState(false);
  const [options, setOptions] = React.useState([]);
  const loading = open && options.length === 0;

  const classes = useStyles();

  React.useEffect(() => {
    let active = true;

    if (!loading) {
      return undefined;
    }

    (async () => {
      const text = await Network.getOptions();
      //const response = await fetch('https://country.register.gov.uk/records.json?page-size=5000');
      //await sleep(1e3); // For demo purposes.
      //const countries = await response.json();
      const list = await text.json();

      if (active) {
        setOptions(list);
      }
    })();

    return () => {
      active = false;
    };
  }, [loading]);

  React.useEffect(() => {
    if (!open) {
      setOptions([]);
    }
  }, [open]);

  return (
    <Autocomplete
      id="asynchronous"
      style={{ width: 300 }}
      open={open}
      onOpen={() => {
        setOpen(true);
      }}
      onClose={() => {
        setOpen(false);
      }}
      classes={{
        root: classes.inputRoot,
        input: classes.inputInput,
      }}
      getOptionSelected={(option, value) => option === value}
      getOptionLabel={option => option}
      options={options}
      loading={loading}
      freeSolo
      classes={{
        root: classes.inputRoot,
        input: classes.inputInput,
      }}
      renderInput={params => (
        <TextField
          {...params}
          label="Search"
          variant="outlined"
          fullWidth
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <React.Fragment>
                {loading ? <CircularProgress color="inherit" size={20} /> : null}
                {params.InputProps.endAdornment}
              </React.Fragment>
            ),
          }}
        />
      )}
    />
  );
}