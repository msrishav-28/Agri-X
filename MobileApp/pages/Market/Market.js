import React from 'react';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar, StyleSheet, View, Dimensions } from 'react-native';
import MarketPrices from './MarketPrices';
import NearbyStores from './NearbyStores';
import PriceComparison from './PriceComparison';
import MarketInsights from './MarketInsights';
import { theme } from '../../theme.config';
import Header from '../../components/Header';

const Tab = createMaterialTopTabNavigator();
const { width, height } = Dimensions.get('window');

const Market = () => {
  return (
    <View style={Styles.container}>
      <StatusBar translucent backgroundColor="transparent" barStyle="dark-content" />
      {/* Background Gradient Orbs */}
      <View
        style={{
          position: 'absolute',
          top: -50,
          right: -100,
          width: 300,
          height: 300,
          backgroundColor: theme.secondary + '10',
          borderRadius: 150,
        }}
      />
      <View
        style={{
          position: 'absolute',
          bottom: 100,
          left: -50,
          width: 250,
          height: 250,
          backgroundColor: theme.primary + '10',
          borderRadius: 125,
        }}
      />

      <Tab.Navigator
        screenOptions={{
          tabBarActiveTintColor: theme.primary,
          tabBarInactiveTintColor: theme.text3,
          tabBarStyle: {
            backgroundColor: 'rgba(255,255,255,0.8)',
            elevation: 0,
            shadowOpacity: 0,
            borderBottomWidth: 1,
            borderBottomColor: theme.border,
            marginTop: 0,
          },
          tabBarIndicatorStyle: {
            backgroundColor: theme.primary,
            height: 3,
            borderRadius: 3,
          },
          tabBarLabelStyle: {
            fontFamily: theme.font.bold,
            fontSize: theme.fs6,
            textTransform: 'none',
          },
          tabBarPressColor: theme.primary + '20',
        }}
        sceneContainerStyle={{ backgroundColor: 'transparent' }}
      >
        <Tab.Screen
          name="Prices"
          component={MarketPrices}
          options={{ tabBarLabel: 'Current Prices' }}
        />
        <Tab.Screen
          name="Stores"
          component={NearbyStores}
          options={{ tabBarLabel: 'Nearby Stores' }}
        />
        {/* <Tab.Screen
          name="Compare"
          component={PriceComparison}
          options={{ tabBarLabel: 'Compare' }}
        />
        <Tab.Screen
          name="Insights"
          component={MarketInsights}
          options={{ tabBarLabel: 'AI Insights' }}
        /> */}
      </Tab.Navigator>
    </View>
  );
};

export default Market;

const Styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.bg,
    paddingTop: StatusBar.currentHeight,
  },
})