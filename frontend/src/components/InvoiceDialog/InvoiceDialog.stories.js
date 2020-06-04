import React from 'react';
import { action } from '@storybook/addon-actions';
import InvoiceDialog from "components/InvoiceDialog/InvoiceDialog";

export default {
  title: 'InvoiceDialog',
  component: InvoiceDialogStory,
};

export const InvoiceDialogStory = () => (

  <InvoiceDialog invoiceID={1} onClose={null} open={true}/>

);
