import React from 'react';
import { action } from '@storybook/addon-actions';
import InfoColumn from "components/InfoColumn/InfoColumn";
import GridContainer from "components/Grid/GridContainer";

export default {
  title: 'InfoColumn',
  component: InfoColumnStory,
};

export const InfoColumnStory = () => (
    <GridContainer>
        <InfoColumn label={"Test Label long"} id={"test_id"} value={"Test Value"} sm={12} xs={12} md={12} />
        <InfoColumn label={"Test Label medium"} id={"test_id"} value={"Test Value"} sm={12} xs={12} md={6} />
        <InfoColumn label={"Test Label medium"} id={"test_id"} value={"Test Value"} sm={12} xs={12} md={6} />
        <InfoColumn label={"Test Label short"} id={"test_id"} value={"Test Value"} sm={12} xs={12} md={3} />
        <InfoColumn label={"Test Label short"} id={"test_id"} value={"Test Value"} sm={12} xs={12} md={3} />
        <InfoColumn label={"Test Label short"} id={"test_id"} value={"Test Value"} sm={12} xs={12} md={3} />
    </GridContainer>
);
