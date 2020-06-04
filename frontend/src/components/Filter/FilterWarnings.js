import React, { useState} from "react";
import {useForm} from "react-hook-form"
// nodejs library to set properties for components
import PropTypes from "prop-types";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import ExpansionPanelSummary from "@material-ui/core/ExpansionPanelSummary";
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpansionPanelDetails from "@material-ui/core/ExpansionPanelDetails";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import TextField from "@material-ui/core/TextField";
import {IconButton} from "@material-ui/core";
import ExpansionPanel from "@material-ui/core/ExpansionPanel";
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";

import SearchIcon from '@material-ui/icons/Search';
import {blackColor} from "../../assets/jss/material-dashboard-react";

const styles = {
  cardCategoryWhite: {
    "&,& a,& a:hover,& a:focus": {
      color: "rgba(255,255,255,.62)",
      margin: "0",
      fontSize: "14px",
      marginTop: "0",
      marginBottom: "0"
    },
    "& a,& a:hover,& a:focus": {
      color: "#FFFFFF"
    }
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none",
    "& small": {
      color: "#777",
      fontSize: "65%",
      fontWeight: "400",
      lineHeight: "1"
    }
  },
  cardTitleWhiteCenter: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none",
    "& small": {
      color: "#777",
      fontSize: "65%",
      fontWeight: "400",
      lineHeight: "1"
    },
    justifyContent: "center"
  },
  filterInput: {
    color: "#FFFFFF"
  }
};

const useStyles = makeStyles(styles);

export default function FilterWarnings(props) {
  const classes = useStyles();
  const {register, handleSubmit} = useForm();
  const { ministries, onSubmit } = props;
  const [ministry, setMinistry] = useState(null);
  const [supplierName, setSupplierName] = useState(null);
  const [supplierICO, setSupplierICO] = useState(null);
  const [dateFrom, setDateFrom] = useState(null);
  const [dateTo, setDateTo] = useState(null);

  const onSubmitInner = data => {
    onSubmit({
      "ministry": ministry,
      "supplier_name": supplierName,
      "supplier_ico": supplierICO,
      "date_from": dateFrom,
      "date_to": dateTo
    });
  };

  const getDate = () => {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    return yyyy + '-' + mm + '-' + dd;
  };

  return (
    <ExpansionPanel defaultExpanded={false}>
      <ExpansionPanelSummary
        expandIcon={<ExpandMoreIcon color={blackColor}/>}
        aria-controls="panel1a-content"
        id="panel1a-header"
      >
        Filtry
      </ExpansionPanelSummary>
      <ExpansionPanelDetails>
        <form onSubmit={handleSubmit(onSubmitInner)}>
          <GridContainer>
            <GridItem xs={12} sm={12} md={3}>
              <FormControl color={"primary"} fullWidth={true} name="form_ministry_ico">
                <InputLabel id="filter-ministry-label" name="input_label_ministry">Ministerstvo</InputLabel>
                <Select
                    name="ministry_ico"
                    innerRef={register({minLength: 5})}
                    onChange={e => setMinistry( e.target.value)}
                    value={ministry}
                >
                  <MenuItem key={'0'} value={null}>{null}</MenuItem>
                  {ministries.map(ministry => <MenuItem key={ministry.ministry_ico} value={ministry.ministry_ico}>{ministry.ministry_name}</MenuItem>)}
                </Select>
              </FormControl>
            </GridItem>
            <GridItem xs={12} sm={12} md={3}>
              <FormControl color={"primary"} fullWidth={true}  name="form_date_from">
                <TextField
                  name="date_from"
                  innerRef={register}
                  label="Od"
                  type="date"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  value={dateFrom}
                  onChange={e => setDateFrom( e.target.value)}
                />
              </FormControl>
            </GridItem>
            <GridItem xs={12} sm={12} md={3}>
              <FormControl color={"primary"} fullWidth={true}  name="form_date_to">
                <TextField
                  name="date_to"
                  innerRef={register}
                  label="Do"
                  type="date"
                  InputLabelProps={{
                    shrink: true,
                  }}
                  defaultValue={getDate()}
                  value={dateTo}
                  onChange={e => setDateTo( e.target.value)}
                />
              </FormControl>
            </GridItem>
            <GridItem xs={12} sm={12} md={5}>
              <FormControl color={"primary"} fullWidth={true} name="form_supplier_ico">
                <TextField
                    name="supplier_name"
                    innerRef={register({minLength: 5})}
                    onChange={e => setSupplierName( e.target.value)}
                    label="Jméno dodavatele"
                    value={supplierName}
                />
              </FormControl>
            </GridItem>
            <GridItem xs={12} sm={12} md={5}>
               <FormControl color={"primary"} fullWidth={true} name="form_supplier_ico">
                <TextField
                    name="supplier_ico"
                    innerRef={register}
                    onChange={e => setSupplierICO( e.target.value)}
                    label="IČO dodavatele"
                    value={supplierICO}
                />
              </FormControl>
            </GridItem>
            <GridItem xs={12} sm={12} md={2}>
              <IconButton color="primary" type="submit">
                <SearchIcon/>
              </IconButton>
            </GridItem>
          </GridContainer>
        </form>
      </ExpansionPanelDetails>
    </ExpansionPanel>
  );
}

FilterWarnings.propTypes = {
  ministries: PropTypes.arrayOf(PropTypes.shape({
    ministry_ico: PropTypes.string,
    ministry_name: PropTypes.string
  })),
  onSubmit: PropTypes.func
};
