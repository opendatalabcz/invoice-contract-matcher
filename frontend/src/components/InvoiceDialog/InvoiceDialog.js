import React, {useEffect, useState} from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
// core components
import GridContainer from "components/Grid/GridContainer.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";

import PropTypes from 'prop-types';
import IconButton from '@material-ui/core/IconButton';
import Dialog from '@material-ui/core/Dialog';
import InfoColumn from "components/InfoColumn/InfoColumn";
//variables
import {matcher_api_url} from "variables/general";

const styles = {
  cardCategoryWhite: {
    color: "rgba(255,255,255,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none"
  },
  whiteIcon:{
    color: "#FFFFFF"}

};

const useStyles = makeStyles(styles);

export default function InvoiceDialog(props) {
  const classes = useStyles();
  const { onClose, contractID, open } = props;
  const [hasError, setErrors] = useState(false);
  const [invoice, setInvoice] = useState({});

  useEffect(() => {
    fetchData();
  },[props]);

  async function fetchData() {
    if(props.invoiceID !== null){
      const res = await fetch(matcher_api_url + "/invoices/" + props.invoiceID);
      res
          .json()
          .then(res => setInvoice(res.invoice))
          .catch(err => setErrors(err));
    }
  }

  const getNumberInPretyString = (number) => {
    if(number){
      return parseFloat(String(number)).toLocaleString('cs-CZ', {style: "currency", currency: "CZK"})
    } else {
      return ''
    }
  };

  const getAttributeArray = (invoice) => {
    return [
      {label:"Ministerstvo", id:"ministerstvo", value:invoice.ministry_name},
      {label:"Dodavatel", id:"dodavatel", value:invoice.supplier_name},
      {label:"IČO Ministerstva", id:"ministerstvo_ico", value:invoice.ministry_ico},
      {label:"IČO Dodavatele", id:"dodavatel_ico", value:invoice.supplier_ico},
      {label:"Částka s DPH", id:"castka_s_dph", value:getNumberInPretyString(invoice.amount_with_dph)},
      {label:"Částka bez DPH", id:"castka_bez_dph", value:getNumberInPretyString(invoice.amount_without_dph)},
      {label:"Částka v cizí měně", id:"castka_v_cizi_mene", value:invoice.amount_different_currency},
      {label:"Měna", id:"mena", value:invoice.currency},
      {label:"Datum vystavení", id:"datum_vystaveni", value:invoice.date_issue},
      {label:"Datum přijetí", id:"datum_prijeti", value:invoice.date_acceptance},
      {label:"Datum zaplacení", id:"datum_zaplaceni", value:invoice.date_payment},
      {label:"Datum splatnosti", id:"datum_splatnosti", value:invoice.date_due},
      {label:"Číslo smlouvy", id:"cislo_smlouvy", value:invoice.contract_number},
      {label:"Variabilní symbol", id:"variabilni_symbol", value:invoice.variable_symbol},
      {label:"Číslo dokumentu", id:"cislo_documentu", value:invoice.document_number},
      {label:"Označení dokumentu", id:"oznaceni_dokumentu", value:invoice.document_label},
      {label:"Identifikátor faktury", id:"identifikator_faktury", value:invoice.external_id},
      {label:"Kód rozpočtové položky", id:"kod_rozpoctove_polozky", value:invoice.budget_item_code},
      {label:"Rozpočtová položka", id:"rozpoctova_polozka", value:invoice.budget_item_name},
      {label:"Kód rozpočtové položky", id:"kod_rozpoctove_polozky", value:invoice.document_label},
      {label:"Předmět faktury", id:"predmet", value:invoice.purpose, md:12}
    ]
  };

  const handleClose = () => {
    onClose();
  };

  return (
    <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open}>
      <Card>
        <CardHeader color="primary">
          <h4 className={classes.cardTitleWhite}>
              Faktura č.{invoice.invoice_id}
            <IconButton className={classes.whiteIcon} onClick={() => window.location.href="/matcher/invoice/"+invoice.invoice_id}><ArrowForwardIosIcon/></IconButton>
          </h4>
        </CardHeader>
        <CardBody>
          <GridContainer>
          {getAttributeArray(invoice).map(attribute => (
                  <InfoColumn label={attribute.label} id={attribute.id} value={attribute.value}
                    xs={attribute.xs ?? 12} sm={attribute.sm ?? 12} md={attribute.md ?? 6} />
          ))}
          </GridContainer>
        </CardBody>
      </Card>
    </Dialog>
  );
}
InvoiceDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  invoiceID: PropTypes.number
};

