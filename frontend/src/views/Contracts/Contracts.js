import React, {useEffect, useState} from "react";
// @material-ui/core components
import { IconButton, LinearProgress, Badge } from '@material-ui/core';
import { makeStyles } from "@material-ui/core/styles";
import {red} from "@material-ui/core/colors";
import {FeaturedPlayList, KeyboardArrowLeft, KeyboardArrowRight, LinkOff} from '@material-ui/icons';
// core components
import GridItem from "components/Grid/GridItem";
import GridContainer from "components/Grid/GridContainer";
import Table from "components/Table/Table";
import Card from "components/Card/Card";
import CardHeader from "components/Card/CardHeader";
import CardBody from "components/Card/CardBody";
import Filter from "components/Filter/Filter";
//variables
import {matcher_api_url} from "variables/general"

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
  }
};

const useStyles = makeStyles(styles);

export default function Contracts() {
  const classes = useStyles();
  const [hasError, setErrors] = useState(false);
  const [contracts, setContracts] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [reload, setReload] = useState(false);

  let search = new URLSearchParams(window.location.search);
  const [ministries, setMinistries] = useState([]);
  const [filterMinistry, setFilterMinistry] = useState(search.get("m_ico") !== undefined ? search.get("m_ico")  : null);
  const [filterSupplierName, setFilterSupplierName] = useState(search.get("s_name") !== undefined ? search.get("s_name") : null);
  const [filterSupplierICO, setFilterSupplierICO] = useState(search.get("s_ico") !== undefined ? search.get("s_ico") : null);
  const [filterDateFrom, setFilterDateFrom] = useState(search.get("date_to") !== undefined  ? search.get("date_to") : null);
  const [filterDateTo, setFilterDateTo] = useState(search.get("date_from") !== undefined  ? search.get("date_from") : null);
  const [filterOnlyLinked, setFilterOnlyLinked] = useState(search.get("linked") !== undefined  ? search.get("linked") : null);

  async function fetchData() {
    setLoading(true);

    //get ministeries
    var murl = new URL(matcher_api_url+ "/ministry");
    const mres = await fetch(murl);
    mres
      .json()
      .then(res => setMinistries(res.ministry))
      .catch(err => setErrors(err));


    var url = new URL(matcher_api_url + "/contracts/page"),
    params = {
      page:page,
      m_ico:filterMinistry,
      s_ico:filterSupplierICO,
      s_name:filterSupplierName,
      from:filterDateFrom,
      to:filterDateTo,
      linked:filterOnlyLinked
    };

    Object.keys(params).forEach(key => params[key] !== null ? url.searchParams.append(key, params[key]) : null);

    const res = await fetch(url);
    res
      .json()
      .then(res => setContracts(res.contracts.map((c) =>
          [
              c.ministry_name,
            c.supplier_name,
            c.purpose,
            c.date_agreed,
            getNumberInPretyString(c.amount),
            <IconButton color="primary" onClick={() => window.location.href="/matcher/contract/"+c.contract_id}>
              <Badge badgeContent={c.linked ? c.linked : <LinkOff fontSize="small" style={{ color: red[500] }}/>}>
                <FeaturedPlayList/>
              </Badge>
            </IconButton>])))
      .catch(err => setErrors(err));
    setLoading(false);
  }

  useEffect(() => {
    fetchData();
  },[reload]);

  function nextPage() {
    let new_page = page + 1;
    setPage(new_page);
    fetchData()
  }

  function previousPage() {
    let new_page = page - 1;
    if (new_page < 1) {new_page = 1}
    setPage(new_page);
    fetchData()
  }

  const handleFilterSubmit = (data) => {
    setFilterMinistry(data.ministry);
    setFilterSupplierName(data.supplier_name);
    setFilterSupplierICO(data.supplier_ico);
    setFilterDateFrom(data.date_from);
    setFilterDateTo(data.date_to);
    setFilterOnlyLinked(data.only_linked);
    setReload(!reload);
  };

  const getNumberInPretyString = (number) => {
    if(number){
      return parseFloat(String(number)).toLocaleString('cs-CZ', {style: "currency", currency: "CZK"})
    } else {
      return ''
    }
  };

  return (
    <GridContainer>
      <GridItem xs={12} sm={12} md={12}>
        <Card>
          <CardHeader color="primary" className={classes.cardTitleWhite}>
            <h4 className={classes.cardTitleWhite}>Smlouvy
            <IconButton className={classes.cardTitleWhite} onClick={previousPage}>
              <KeyboardArrowLeft/>
            </IconButton>
              Strana: {page}
            <IconButton className={classes.cardTitleWhite} onClick={nextPage}>
            <KeyboardArrowRight/>
            </IconButton>
              {loading ? <LinearProgress /> : null}
            </h4>
          </CardHeader>
          <CardBody>
            <Filter onSubmit={handleFilterSubmit}
                    ministries={ministries}
                    ministry={filterMinistry}
                    supplier_name={filterSupplierName}
                    supplier_ico={filterSupplierICO}
                    date_from={filterDateFrom}
                    date_to={filterDateTo}
                    linked={filterOnlyLinked}
            />
            <Table
              tableHeaderColor="primary"
              tableHead={["Ministerstvo", "Dodavatel", "Předmět", "Datum uzavření", "Částka", "Přesměrování"]}
              tableData={
                contracts
              }
            />
          </CardBody>
        </Card>
      </GridItem>
    </GridContainer>
  );
}
