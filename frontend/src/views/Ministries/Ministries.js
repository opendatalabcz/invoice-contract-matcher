import React, {useEffect, useState} from "react";
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import Icon from "@material-ui/core/Icon";
// @material-ui/icons
import {Assessment, FeaturedPlayList, Description} from '@material-ui/icons';
// core components
import GridItem from "components/Grid/GridItem";
import GridContainer from "components/Grid/GridContainer";
import CustomTabs from "components/CustomTabs/CustomTabs";
import Card from "components/Card/Card";
import CardHeader from "components/Card/CardHeader";
import CardIcon from "components/Card/CardIcon";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle";

import {matcher_api_url} from "variables/general";

import {
  contractsMonthlyMinistryChart,
} from "variables/charts";
import {IconButton} from "@material-ui/core";

const useStyles = makeStyles(styles);


export default function Ministries() {
  const classes = useStyles();
  const [hasError, setErrors] = useState(false);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  async function fetchData() {
    setLoading(true);
    const res = await fetch(matcher_api_url + "/statistics/ministry_data");
    res
      .json()
      .then(res => setData(res.data))
      .catch(err => setErrors(err));
    setLoading(false);
  }

  useEffect(() => {

    fetchData();
  },[]);

  return (
    <div>

      <GridContainer>
        {data.map(ministry => (
          <GridItem xs={12} sm={12} key={ministry.ministry_name}>
            <CustomTabs
                title={ministry.ministry_name}
                headerColor="primary"
                tabs={[
                    {
                    tabName: "Statistiky",
                    tabIcon: Assessment,
                    tabContent: (
                      <GridContainer>
                        <GridItem xs={12} sm={6} md={3}>
                          <Card>
                            <CardHeader color="success" stats icon>
                              <CardIcon color="success">
                                <IconButton size={'small'} onClick={() => window.location.href="/matcher/invoices?m_ico="+ministry.ministry_ico}><Icon style={{ color: 'white' }}>description</Icon></IconButton>
                              </CardIcon>
                              <p className={classes.cardCategory}>Faktury</p>
                              <h3 className={classes.cardTitle}>
                                {ministry.invoice_count === undefined ? 0 : ministry.invoice_count.toLocaleString('en-US').replace(',', ' ')}
                              </h3>
                            </CardHeader>
                          </Card>
                        </GridItem>
                        <GridItem xs={12} sm={6} md={3}>
                          <Card>
                            <CardHeader color="success" stats icon>
                              <CardIcon color="success">
                                <IconButton size={'small'} onClick={() => window.location.href="/matcher/contracts?m_ico="+ministry.ministry_ico}><Icon style={{ color: 'white' }}>list_alt</Icon></IconButton>
                              </CardIcon>
                              <p className={classes.cardCategory}>Smlouvy</p>
                              <h3 className={classes.cardTitle}>
                                {ministry.contract_count === undefined ? 0 : ministry.contract_count.toLocaleString('en-US').replace(',', ' ')}
                              </h3>
                            </CardHeader>
                          </Card>
                        </GridItem>
                        <GridItem xs={12} sm={6} md={3}>
                          <Card>
                            <CardHeader color="danger" stats icon>
                              <CardIcon color="danger">
                                <IconButton size={'small'} onClick={() => window.location.href="/matcher/warnings?m_ico="+ministry.ministry_ico}><Icon style={{ color: 'white' }}>warning</Icon></IconButton>
                              </CardIcon>
                              <p className={classes.cardCategory}>Podezřelé</p>
                              <h3 className={classes.cardTitle}>
                                {ministry.warnings_count === undefined ? 0 : ministry.warnings_count.toLocaleString('en-US').replace(',', ' ')}
                              </h3>
                            </CardHeader>
                          </Card>
                        </GridItem>
                        <GridItem xs={12} sm={6} md={3}>
                          <Card>
                            <CardHeader color="info" stats icon>
                              <CardIcon color="info">
                                <IconButton size={'small'} onClick={() => window.location.href="/matcher/contracts?m_ico="+ministry.ministry_ico+"&linked=true"}><Icon style={{ color: 'white' }}>link</Icon></IconButton>
                              </CardIcon>
                              <p className={classes.cardCategory}>Spojeno</p>
                              <h3 className={classes.cardTitle}>
                                {ministry.linked_count === undefined ? 0 : ministry.linked_count.toLocaleString('en-US').replace(',', ' ')}
                              </h3>
                            </CardHeader>
                          </Card>
                        </GridItem>
                      </GridContainer>
                    )
                  },
                  {
                    tabName: "Smlouvy",
                    tabIcon: FeaturedPlayList,
                    tabContent: (
                        <GridContainer>
                            <GridItem xs={12} sm={12} md={12}>
                              <Card chart>
                                <CardHeader color="primary">
                                    {ministry.contract_count_monthly.counts.length === 0 ? "Nejsou data" :
                                      <ChartistGraph
                                        className="ct-chart"
                                        data={{series: [ministry.contract_count_monthly.counts],labels:ministry.contract_count_monthly.months}}
                                        type="Line"
                                        options={contractsMonthlyMinistryChart.options}
                                        listener={contractsMonthlyMinistryChart.animation}
                                      />
                                    }
                                </CardHeader>
                              </Card>
                            </GridItem>
                        </GridContainer>
                    )
                  },
                  {
                    tabName: "Faktury",
                    tabIcon: Description,
                    tabContent: (
                      <GridContainer>
                            <GridItem xs={12} sm={12} md={12}>
                              <Card chart>
                                  <CardHeader color="matcher">
                                      {ministry.invoice_count_monthly.counts.length === 0 ? "Nejsou data" :
                                      <ChartistGraph
                                          className="ct-chart"
                                          data={{
                                              series: [ministry.invoice_count_monthly.counts],
                                              labels: ministry.invoice_count_monthly.months
                                          }}
                                          type="Line"
                                          options={contractsMonthlyMinistryChart.options}
                                          listener={contractsMonthlyMinistryChart.animation}
                                      />}
                                  </CardHeader>
                              </Card>
                            </GridItem>
                      </GridContainer>
                    )
                  },
                ]}
              />
          </GridItem>
        ))}
      </GridContainer>
    </div>
  );
}
