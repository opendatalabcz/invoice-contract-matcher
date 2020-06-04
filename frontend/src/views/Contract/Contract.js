import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";
import Link from "@material-ui/core/Link";
import InvoiceDialog from "components/InvoiceDialog/InvoiceDialog";
import {matcher_api_url} from "variables/general"
import {Button, IconButton} from "@material-ui/core";
import LinearProgress from "@material-ui/core/LinearProgress";
import Table from "components/Table/Table.js";
import {FindInPage} from "@material-ui/icons";
import Icon from "@material-ui/core/Icon";
import CardIcon from "components/Card/CardIcon";
import InfoColumn from "components/InfoColumn/InfoColumn";
import Tooltip from "@material-ui/core/Tooltip";
import Typography from "@material-ui/core/Typography";

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
  cardCategoryBlack: {
    color: "rgba(0,0,0,.62)",
    margin: "0",
    fontSize: "14px",
    marginTop: "0",
    marginBottom: "0"
  },
  cardTitleBlack: {
    color: "#000000",
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

export default function Contract() {

  const [hasError, setErrors] = useState(false);

  const [contract, setContract] = useState({});

  const [selectedID, setselectedID] = useState(useParams().contract_id);
  const [selectedInvoiceID, setSelectedInvoiceID] = useState(null);
  const [finalRelations, setFinalRelations] = useState([[]]);
  const [relations, setRelations] = useState([[]]);
  const [finalRelationsAmount, setFinalRelationsAmount] = useState('...');
  const [contractAmount, setContractAmount] = useState('...');


  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const classes = useStyles();

  const handleClickOpen = (id) => {
    setSelectedInvoiceID(id);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  async function fetchData() {
    setLoading(true);
    const res = await fetch(matcher_api_url + "/contracts/" + selectedID);
    res
      .json()
      .then(res => {
          setContract(res.contract);
          setContractAmount(Math.max.apply(Math, [res.contract.amount_with_dph, res.contract.amount_without_dph]));
      })
      .catch(err => setErrors(err));
    const rels = await fetch(matcher_api_url + "/relations/contract/" + selectedID);
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
              <IconButton color="primary" onClick={() => handleClickOpen(i.invoice_id)}>
                <FindInPage/>
              </IconButton>]));

          setFinalRelations(res.final_relations.map((i) => [
              i.ministry_name,
              i.supplier_name,
              i.purpose,
              i.date_issue,
              getNumberInPretyString(i.amount),
              i.score,
              <IconButton color="primary" onClick={() => handleClickOpen(i.invoice_id)}>
                <FindInPage/>
              </IconButton>]));
          setFinalRelationsAmount(res.final_relations.map((i) => i.amount).reduce((a, b) => a+b, 0));
      })
      .catch(err => setErrors(err));
      setLoading(false);
  }

  useEffect(() => {
    fetchData();

  },[]);

  const getNumberInPretyString = (number) => {
    if(number){
      return parseFloat(String(number)).toLocaleString('cs-CZ', {style: "currency", currency: "CZK"})
    } else {
      return ''
    }
  };

  const getDateInPretyString = (value) => {
    if(value){
      return new Date(value).toLocaleDateString().split("/").join(".")
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
      {label:"Datum uzavření",            id:"datum_uzavreni", value:getDateInPretyString(contract.date_agreed)},
      {label:"Datum vystavení v Registru smluv", id:"datum_prijeti", value:getDateInPretyString(contract.date_published)},
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
    <div>
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Smlouva č.{contract.contract_id}</h4>
              <p className={classes.cardCategoryWhite}>{contract.purpose}</p>
            </CardHeader>
            <CardBody>
              <GridContainer>
              {getAttributeArray(contract).map(attribute => (
                  <InfoColumn label={attribute.label} id={attribute.id} value={attribute.value}
                    xs={attribute.xs ?? 12} sm={attribute.sm ?? 12} md={attribute.md ?? 6} />
              ))}
              </GridContainer>

            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
      <GridContainer>
        <GridItem xs={12} sm={12} md={4}>
          <Card>
            <CardHeader color="success" stats icon>
              <CardIcon color="success">
                <Icon>description</Icon>
              </CardIcon>
              <p className={classes.cardTitleBlack}>Počet navázaných faktur</p>
              <h3 className={classes.cardTitleBlack}>
                {finalRelations.length}
              </h3>
            </CardHeader>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={12} md={4}>
          <Card>
            <CardHeader color={finalRelationsAmount > contractAmount ? "warning" : "success"} stats icon>
              <CardIcon color={finalRelationsAmount > contractAmount ? "warning" : "success"}>
                <Icon>file_copy</Icon>
              </CardIcon>
              <p className={classes.cardTitleBlack}>Hodnota navázaných faktur</p>
              <h3 className={classes.cardTitleBlack}>
                {getNumberInPretyString(finalRelationsAmount)}
              </h3>
            </CardHeader>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={12} md={4}>
          <Card>
            <CardHeader color="success" stats icon>
              <CardIcon color="success">
                <Icon>list_alt</Icon>
              </CardIcon>
              <p className={classes.cardTitleBlack}>Hodnota smlouvy</p>
              <h3 className={classes.cardTitleBlack}>
                {getNumberInPretyString(contractAmount)}
              </h3>
            </CardHeader>
          </Card>
        </GridItem>
      </GridContainer>
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={classes.cardTitleWhite}>Faktury
              {loading ? <LinearProgress /> : null}
              </h4>
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
              <h4 className={classes.cardTitleWhite}>Další faktury
              {loading ? <LinearProgress /> : null}
              </h4>
            </CardHeader>
            <CardBody>
              <Table
                tableHeaderColor="primary"
                tableHead={["Ministerstvo", "Dodavatel", "Předmět", "Datum vystavení", "Částka", "Score", "Akce"]}
                tableData={relations}
              />
            </CardBody>
            <InvoiceDialog invoiceID={selectedInvoiceID} open={open} onClose={handleClose}/>
          </Card>
        </GridItem>
      </GridContainer>
    </div>
  );
}
