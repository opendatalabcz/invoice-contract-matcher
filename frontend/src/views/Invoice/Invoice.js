import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
import {IconButton, LinearProgress} from "@material-ui/core";
// @material-ui/icons components
import {FindInPage} from "@material-ui/icons";
// core components
import GridItem from "components/Grid/GridItem";
import GridContainer from "components/Grid/GridContainer";
import Card from "components/Card/Card";
import CardHeader from "components/Card/CardHeader";
import CardBody from "components/Card/CardBody";
import ContractDialog from "components/ContractDialog/ContractDialog";
import Table from "components/Table/Table";
import InfoColumn from "components/InfoColumn/InfoColumn";
//variables
import {matcher_api_url} from "variables/general"

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

export default function Invoice() {

  const [hasError, setErrors] = useState(false);

  const [invoice, setInvoice] = useState({});

  const [selectedInvoiceID, setSelectedInvoiceID] = React.useState(useParams().invoice_id);
  const [selectedContractID, setSelectedContractID] = React.useState(null);
  const [finalRelations, setFinalRelations] = useState([]);
  const [relations, setRelations] = useState([]);

  const [loading, setLoading] = useState(false);
  const [open, setOpen] = React.useState(false);

  const classes = useStyles();

  const handleClickOpen = (id) => {
    setSelectedContractID(id);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const getAttributeArray = (invoice) => {
    return [
      {label:"Ministerstvo", id:"ministerstvo", value:invoice.ministry_name},
      {label:"Dodavatel", id:"dodavatel", value:invoice.supplier_name},
      {label:"IČO Ministerstva", id:"ministerstvo_ico", value:invoice.ministry_ico},
      {label:"IČO Dodavatele", id:"dodavatel_ico", value:invoice.supplier_ico},
      {label:"Částka s DPH", id:"castka_s_dph", value:getNumberInPretyString(invoice.amount_with_dph), md:3},
      {label:"Částka bez DPH", id:"castka_bez_dph", value:getNumberInPretyString(invoice.amount_without_dph), md:3},
      {label:"Částka v cizí měně", id:"castka_v_cizi_mene", value:invoice.amount_different_currency, md:3},
      {label:"Měna", id:"mena", value:invoice.currency, md:3},
      {label:"Datum vystavení", id:"datum_vystaveni", value:invoice.date_issue, md:3},
      {label:"Datum přijetí", id:"datum_prijeti", value:invoice.date_acceptance, md:3},
      {label:"Datum zaplacení", id:"datum_zaplaceni", value:invoice.date_payment, md:3},
      {label:"Datum splatnosti", id:"datum_splatnosti", value:invoice.date_due, md:3},
      {label:"Číslo smlouvy", id:"cislo_smlouvy", value:invoice.contract_number, md:3},
      {label:"Variabilní symbol", id:"variabilni_symbol", value:invoice.variable_symbol, md:3},
      {label:"Číslo dokumentu", id:"cislo_documentu", value:invoice.document_number, md:3},
      {label:"Označení dokumentu", id:"oznaceni_dokumentu", value:invoice.document_label, md:3},
      {label:"Identifikátor faktury", id:"identifikator_faktury", value:invoice.external_id, md:3},
      {label:"Kód rozpočtové položky", id:"kod_rozpoctove_polozky", value:invoice.budget_item_code, md:3},
      {label:"Rozpočtová položka", id:"rozpoctova_polozka", value:invoice.budget_item_name, md:3},
      {label:"Kód rozpočtové položky", id:"kod_rozpoctove_polozky", value:invoice.document_label, md:3},
      {label:"Předmět faktury", id:"predmet", value:invoice.purpose, md:12}
    ]
  };

  async function fetchData() {
    setLoading(true);
    const res = await fetch(matcher_api_url + "/invoices/" + selectedInvoiceID);
    res
      .json()
      .then(res => setInvoice(res.invoice))
      .catch(err => setErrors(err));
    const rels = await fetch(matcher_api_url + "/relations/invoice/" + selectedInvoiceID);
    rels
      .json()
      .then(res => {
        setRelations(res.relations.map((i) => [
          i.ministry_name,
          i.supplier_name,
          i.purpose,
          i.date_issue,
          getNumberInPretyString(i.amount),
          i.score,
          <IconButton color="primary" onClick={() => handleClickOpen(i.contract_id)}>
            <FindInPage/>
          </IconButton>]));
        setFinalRelations(res.final_relations.map((i) => [
          i.ministry_name,
          i.supplier_name,
          i.purpose,
          i.date_issue,
          getNumberInPretyString(i.amount),
          i.score,
          <IconButton color="primary" onClick={() => handleClickOpen(i.contract_id)}>
            <FindInPage/>
          </IconButton>]));
      })
      .catch(err => setErrors(err));
    setLoading(false);
  }

  const getNumberInPretyString = (number) => {
    if(number){
      return parseFloat(String(number)).toLocaleString('cs-CZ', {style: "currency", currency: "CZK"})
    } else {
      return ''
    }
  };

  const getDateInPretyString = (value) => {
    if(value){
      return new Date(value).toLocaleDateString()
    } else {
      return ''
    }
  };

  useEffect(() => {
    fetchData();
  },[]);

  return (
    <div>
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Faktura č.{invoice.invoice_id}</h4>
              <p className={classes.cardCategoryWhite}>{invoice.purpose}</p>
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
        </GridItem>
      </GridContainer>
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Navázaná smlouva</h4>
              <p className={classes.cardCategoryWhite}>Smlouva, která byla přiřazena k faktuře</p>
              {loading ? <LinearProgress /> : null}
            </CardHeader>
            <CardBody>
              <Table
                tableHeaderColor="primary"
                tableHead={["Ministerstvo", "Dodavatel", "Předmět", "Datum vystavení", "Částka", "Score", "Akce"]}
                tableData={finalRelations}
              />
            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Další smlouvy</h4>
              <p className={classes.cardCategoryWhite}>Smlouvy, která mohou být navázány k této faktuře</p>
              {loading ? <LinearProgress /> : null}
            </CardHeader>
            <CardBody>
              <Table
                tableHeaderColor="primary"
                tableHead={["Ministerstvo", "Dodavatel", "Předmět", "Datum vystavení", "Částka", "Score", "Akce"]}
                tableData={relations}
              />
            </CardBody>
            <ContractDialog contractID={selectedContractID} open={open} onClose={handleClose}/>
          </Card>
        </GridItem>
      </GridContainer>
    </div>
  );
}





