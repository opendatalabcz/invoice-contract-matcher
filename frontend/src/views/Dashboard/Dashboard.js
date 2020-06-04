import React, {useEffect, useState} from "react";
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import {Icon, IconButton} from "@material-ui/core";
// @material-ui/icons
import {Update} from "@material-ui/icons";
// core components
import GridItem from "components/Grid/GridItem";
import GridContainer from "components/Grid/GridContainer";
import Card from "components/Card/Card";
import CardHeader from "components/Card/CardHeader";
import CardIcon from "components/Card/CardIcon";
import CardBody from "components/Card/CardBody";
import CardFooter from "components/Card/CardFooter";
//variables
import {matcher_api_url} from "variables/general";

import {
  contractsMonthlyChart,
  invoicesMonthlyChart,
  invoiceCountPerMinistryChart,
  contractCountPerMinistryChart
} from "variables/charts";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle";

const useStyles = makeStyles(styles);

export default function Dashboard() {
  const classes = useStyles();
  const [hasError, setErrors] = useState(false);
  const [stats, setStats] = useState(
      {invoice_count: "---",
                contract_count: "---",
                warnings_count: "---",
                linked_count: "---",
                refreshed: "---"
  });
  const [imonthly, setIMonthly] = useState(
      {labels: [],
                series: []
  });
  const [cmonthly, setCMonthly] = useState(
      {labels: [],
                series: []
  });
  const [iministry, setIMinistry] = useState(
      {labels: [],
                series: []
  });
  const [cministry, setCMinistry] = useState(
      {labels: [],
                series: []
  });

  async function fetchStats() {
    const res = await fetch(matcher_api_url + "/statistics");
    res
      .json()
      .then(res => setStats(res))
      .catch(err => setErrors(err));

  }
  async function fetchMonthlyStats() {
    const ires = await fetch(matcher_api_url + "/statistics/invoices_monthly");
    ires
      .json()
      .then(ires => setIMonthly({labels: ires["months"], series: [ires["invoice_count"]]}))
      .catch(err => setErrors(err));
    const cres = await fetch(matcher_api_url + "/statistics/contracts_monthly");
    cres
      .json()
      .then(cres => setCMonthly({labels: cres["months"], series: [cres["contract_count"]]}))
      .catch(err => setErrors(err));
  }

  async function fetchMinistryStats() {
    const ires = await fetch(matcher_api_url + "/statistics/invoices_ministry");
    ires
      .json()
      .then(ires => setIMinistry({labels: ires["ministry"], series: [ires["invoice_count"]]}))
      .catch(err => setErrors(err));
    const cres = await fetch(matcher_api_url + "/statistics/contracts_ministry");
    cres
      .json()
      .then(cres => setCMinistry({labels: cres["ministry"], series: [cres["contract_count"]]}))
      .catch(err => setErrors(err));
  }

  useEffect(() => {
    fetchStats();
    fetchMinistryStats();
    fetchMonthlyStats();
  },[]);

  return (
    <div>
      <GridContainer>
        <GridItem xs={12} sm={6} md={3}>
          <Card>
            <CardHeader color="success" stats icon>
              <CardIcon color="success">
                <IconButton size={'small'} onClick={() => window.location.href="/matcher/invoices"}><Icon style={{ color: 'white' }}>description</Icon></IconButton>
              </CardIcon>
              <p className={classes.cardCategory}>Počet faktur</p>
              <h3 className={classes.cardTitle}>
                {stats.invoice_count.toLocaleString('en-US').replace(',', ' ')}
              </h3>
            </CardHeader>
            <CardFooter stats>
              <div className={classes.stats}>
                <Update /> Aktualizováno {stats.refreshed}
              </div>
            </CardFooter>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={6} md={3}>
          <Card>
            <CardHeader color="success" stats icon>
              <CardIcon color="success">
                <IconButton size={'small'} onClick={() => window.location.href="/matcher/contracts"}><Icon style={{ color: 'white' }}>list_alt</Icon></IconButton>
              </CardIcon>
              <p className={classes.cardCategory}>Smlouvy</p>
              <h3 className={classes.cardTitle}>{stats.contract_count.toLocaleString('en-US').replace(',', ' ')}</h3>
            </CardHeader>
            <CardFooter stats>
              <div className={classes.stats}>
                <Update />
                Aktualizováno {stats.refreshed}
              </div>
            </CardFooter>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={6} md={3}>
          <Card>
            <CardHeader color="danger" stats icon>
              <CardIcon color="danger">
                <IconButton size={'small'} onClick={() => window.location.href="/matcher/warnings"}><Icon style={{ color: 'white' }}>info_outline</Icon></IconButton>
              </CardIcon>
              <p className={classes.cardCategory}>Podezřelé zakázky</p>
              <h3 className={classes.cardTitle}>{stats.warnings_count.toLocaleString('en-US').replace(',', ' ')}</h3>
            </CardHeader>
            <CardFooter stats>
              <div className={classes.stats}>
                <Update />
                Aktualizováno {stats.refreshed}
              </div>
            </CardFooter>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={6} md={3}>
          <Card>
            <CardHeader color="info" stats icon>
              <CardIcon color="info">
                <IconButton size={'small'} onClick={() => window.location.href="/matcher/invoices"}><Icon style={{ color: 'white' }}>link</Icon></IconButton>
              </CardIcon>
              <p className={classes.cardCategory}>Spojeno</p>
              <h3 className={classes.cardTitle}>{stats.linked_count.toLocaleString('en-US').replace(',', ' ')}</h3>
            </CardHeader>
            <CardFooter stats>
              <div className={classes.stats}>
                <Update />
                Aktualizováno {stats.refreshed}
              </div>
            </CardFooter>
          </Card>
        </GridItem>
      </GridContainer>
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card chart>
            <CardHeader color="primary">
              <ChartistGraph
                className="ct-chart"
                data={iministry}
                type="Bar"
                options={invoiceCountPerMinistryChart.options}
                responsiveOptions={invoiceCountPerMinistryChart.responsiveOptions}
                listener={invoiceCountPerMinistryChart.animation}
              />
            </CardHeader>
            <CardBody>
              <h3 className={classes.cardTitle}>Počet zveřejněných faktur podle ministerstva</h3>
            </CardBody>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={12} md={12}>
          <Card chart>
            <CardHeader color="matcher">
              <ChartistGraph
                className="ct-chart"
                data={cministry}
                type="Bar"
                options={contractCountPerMinistryChart.options}
                responsiveOptions={contractCountPerMinistryChart.responsiveOptions}
                listener={contractCountPerMinistryChart.animation}
              />
            </CardHeader>
            <CardBody>
              <h3 className={classes.cardTitle}>Počet zveřejněných smluv podle ministerstva</h3>
            </CardBody>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={12} md={12}>
          <Card chart>
            <CardHeader color="primary">
              <ChartistGraph
                className="ct-chart"
                data={imonthly}
                type="Line"
                options={invoicesMonthlyChart.options}
                listener={invoicesMonthlyChart.animation}
              />
            </CardHeader>
            <CardBody>
              <h3 className={classes.cardTitle}>Počet zveřejněných faktur měsíčně</h3>
            </CardBody>
          </Card>
        </GridItem>
        <GridItem xs={12} sm={12} md={12}>
          <Card chart>
            <CardHeader color="matcher">
              <ChartistGraph
                className="ct-chart"
                data={cmonthly}
                type="Line"
                options={contractsMonthlyChart.options}
                listener={contractsMonthlyChart.animation}
              />
            </CardHeader>
            <CardBody>
              <h3 className={classes.cardTitle}>Počet zveřejněných smluv měsíčně</h3>
            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
    </div>
  );
}
