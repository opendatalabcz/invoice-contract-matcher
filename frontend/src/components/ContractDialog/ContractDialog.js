import React, {useEffect, useState} from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import InputLabel from "@material-ui/core/InputLabel";
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
// core components
import GridContainer from "components/Grid/GridContainer.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";

import PropTypes from 'prop-types';
import Dialog from '@material-ui/core/Dialog';
import Link from "@material-ui/core/Link";
import InfoColumn from "components/InfoColumn/InfoColumn";
import IconButton from "@material-ui/core/IconButton";

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

export default function ContractDialog(props) {
  const classes = useStyles();
  const { onClose, contractID, open } = props;
  const [hasError, setErrors] = useState(false);
  const [contract, setContract] = useState({});

  useEffect(() => {
    fetchData();
  },[props]);

  async function fetchData() {
    if(props.contractID !== null){
        const res = await fetch("http://127.0.0.1:5000/contracts/" + props.contractID);
        res
          .json()
          .then(res => setContract(res.contract))
          .catch(err => setErrors(err));
    }
  }

  const handleClose = () => {
    onClose();
  };

  const getNumberInPretyString = (number) => {
    if(number){
      return parseFloat(String(number)).toLocaleString('cs-CZ', {style: "currency", currency: "CZK"})
    } else {
      return ''
    }
  };

  const getAttributeArray = (contract) => {
    return [
      {label:"Ministerstvo",              id:"ministerstvo", value:contract.ministry_name},
      {label:"Dodavatel",                 id:"dodavatel", value:contract.supplier_name},
      {label:"IČO Ministerstva",          id:"ministerstvo_ico", value:contract.ministry_ico},
      {label:"IČO Dodavatele",            id:"dodavatel_ico", value:contract.supplier_ico},
      {label:"Adresa ministerstva",       id:"ministerstvo_adresa", value:contract.ministry_address},
      {label:"Adresa dodavatele",         id:"dodavatel_adresa", value:contract.supplier_address},
      {label:"Datová schránka ministerstva", id:"datova_schranka_ministerstva", value:contract.ministry_data_box},
      {label:"Datová schránka dodavatele", id:"datova_schranka_dodavatele", value:contract.supplier_data_box},
      {label:"Částka s DPH",              id:"castka_s_dph", value:getNumberInPretyString(contract.amount_with_dph), md:3},
      {label:"Částka bez DPH",            id:"castka_bez_dph", value:getNumberInPretyString(contract.amount_without_dph), md:3},
      {label:"Částka v cizí měně",        id:"castka_v_cizi_mene", value:getNumberInPretyString(contract.amount_different_currency), md:3},
      {label:"Měna",                      id:"mena", value:getNumberInPretyString(contract.currency), md:3},
      {label:"Datum uzavření",            id:"datum_uzavreni", value:getNumberInPretyString(contract.date_agreed)},
      {label:"Datum vystavení v Registru smluv", id:"datum_prijeti", value:contract.date_published},
      {label:"Číslo smlouvy",             id:"cislo_smlouvy", value:contract.contract_number},
      {label:"Schválil",                  id:"schvalil", value:contract.approved},
      {label:"Link",                      id:"link", value:<Link href={contract.link} target="_blank">{contract.link}</Link>},
      {label:"Platná",                    id:"platna", value:contract.valid},
      {label:"Číslo smlouvy v Registru smluv", id:"cislo_smlouvy_v_registru_smluv", value:contract.external_id},
      {label:"Číslo verze v Registru smluv", id:"cislo_verze_v_registru_smluv", value:contract.version_id},
      {label:"Předmět smlouvy",           id:"predmet_smlouvy", value:contract.purpose, md:12}
    ]
  };

  return (
    <Dialog onClose={handleClose} aria-labelledby="simple-dialog-title" open={open}>
      <Card>
        <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Smlouva č.{contract.contract_id}
                <IconButton className={classes.whiteIcon} onClick={() => window.location.href="/matcher/contract/"+contract.contract_id}><ArrowForwardIosIcon/></IconButton>
              </h4>
        </CardHeader>
        <CardBody>
          <GridContainer>
            {getAttributeArray(contract).map(attribute => (
                  <InfoColumn label={attribute.label} id={attribute.id} value={attribute.value}
                    xs={attribute.xs ?? 12} sm={attribute.sm ?? 12} md={attribute.md ?? 6} />
              ))}
            <InputLabel>{contract.purpose}</InputLabel>
          </GridContainer>
        </CardBody>
      </Card>
    </Dialog>
  );
}
ContractDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  contractID: PropTypes.number
};

