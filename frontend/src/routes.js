/*!

=========================================================
* Material Dashboard React - v1.8.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/material-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
// @material-ui/icons
import Dashboard from "@material-ui/icons/Dashboard";
import AccountBalanceIcon from '@material-ui/icons/AccountBalance';
import WarningIcon from '@material-ui/icons/Warning';
// core components/views for Admin layout
import MinistriesPage from "views/Ministries/Ministries.js";
import DashboardPage from "views/Dashboard/Dashboard.js";
import InvoicesPage from "views/Invoices/Invoices.js";
import ContractsPage from "views/Contracts/Contracts.js";
import WarningsPage from "views/Warnings/Warnings.js";

const dashboardRoutes = [
    {
    path: "/dashboard",
    name: "Přehled",
    icon: Dashboard,
    component: DashboardPage,
    layout: "/matcher"
  },
  {
    path: "/ministries",
    name: "Ministerstva",
    icon: AccountBalanceIcon,
    component: MinistriesPage,
    layout: "/matcher"
  },
  {
    path: "/invoices",
    name: "Faktury",
    icon: "description",
    component: InvoicesPage,
    layout: "/matcher"
  },
  {
    path: "/contracts",
    name: "Smlouvy",
    icon: "featured_play_list",
    component: ContractsPage,
    layout: "/matcher"
  },
  {
    path: "/warnings",
    name: "Podezřelé smlouvy",
    icon: WarningIcon,
    component: WarningsPage,
    layout: "/matcher"
  }
];

export default dashboardRoutes;
