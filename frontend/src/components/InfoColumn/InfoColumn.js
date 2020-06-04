import InputLabel from "@material-ui/core/InputLabel";
import React from "react";
import PropTypes from "prop-types";
import {makeStyles} from "@material-ui/core";
import GridItem from "components/Grid/GridItem";
import CustomInput from "components/CustomInput/CustomInput";

export default function InfoColumn(props) {
    return (
        <GridItem xs={props.xs} sm={props.sm} md={props.md}>
          <CustomInput
            labelText={props.label}
            id={props.id}
            formControlProps={{
              fullWidth: true
            }}
            inputProps={{
              disabled: true
            }}
          />
          <InputLabel>{props.value}</InputLabel>
        </GridItem>
    )
}

InfoColumn.propTypes = {
  label: PropTypes.string,
  id: PropTypes.string,
  value: PropTypes.string,
  xs: PropTypes.number,
  sm: PropTypes.number,
  md: PropTypes.number
};