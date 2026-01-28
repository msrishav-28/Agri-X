import { StyleSheet, Text, View, StatusBar } from 'react-native'
import React from 'react'
import { theme } from '../../theme.config'
import Header from '../../components/Header'
import GlassmorphicCard from '../../components/GlassmorphicCard'

const MarketInsights = () => {
  return (
    <View style={{ flex: 1, backgroundColor: theme.bg }}>
      <StatusBar translucent backgroundColor="transparent" barStyle="dark-content" />
      {/* Background Orbs */}
      <View
        style={{
          position: 'absolute',
          top: -100,
          left: -100,
          width: 300,
          height: 300,
          borderRadius: 150,
          backgroundColor: theme.primary + '15',
        }}
      />
      <View
        style={{
          position: 'absolute',
          bottom: 100,
          right: -50,
          width: 250,
          height: 250,
          backgroundColor: theme.accent + '10',
          borderRadius: 125,
        }}
      />

      <Header text="Market Insights" />

      <View style={{ padding: 24, flex: 1, justifyContent: 'center' }}>
        <GlassmorphicCard style={{ padding: 30, alignItems: 'center' }} blurAmount={5}>
          <Text style={{ fontFamily: theme.font.header, fontSize: theme.fs4, color: theme.primary, marginBottom: 10 }}>
            Market Insights
          </Text>
          <Text style={{ fontFamily: theme.font.regular, fontSize: theme.fs6, color: theme.text2, textAlign: 'center' }}>
            Advanced market analytics and predictions coming soon.
          </Text>
        </GlassmorphicCard>
      </View>
    </View>
  )
}

export default MarketInsights

const styles = StyleSheet.create({})