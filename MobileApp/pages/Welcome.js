import React from 'react';
import {
  View,
  Text,
  Image,
  StyleSheet,
  ScrollView,
  StatusBar,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { theme } from '../theme.config';
import AnimatedButton from '../components/AnimatedButton';
import GlassmorphicCard from '../components/GlassmorphicCard';
import AnimatedFadeInView from '../components/AnimatedFadeInView';

const Welcome = () => {
  const navigation = useNavigation();
  const desc =
    'Join a growing community of farmers, buyers, and agri-experts working together to improve productivity, connect directly, and access real-time insights for better crop management and trade.';

  return (
    <View style={theme.container}>
      <StatusBar translucent backgroundColor="transparent" barStyle="dark-content" />

      {/* Background Gradient Orbs */}
      <View
        style={{
          position: 'absolute',
          top: -50,
          left: -100,
          width: 300,
          height: 300,
          backgroundColor: theme.primary + '15',
          borderRadius: 150,
        }}
      />
      <View
        style={{
          position: 'absolute',
          bottom: 100,
          right: -50,
          width: 250,
          height: 250,
          backgroundColor: theme.secondary + '15',
          borderRadius: 125,
        }}
      />

      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <AnimatedFadeInView animationType="scale" delay={100} style={styles.logoContainer}>
          <Image
            source={require('../assets/images/logo.jpg')}
            style={styles.logo}
          />
        </AnimatedFadeInView>

        <View style={styles.contentContainer}>
          <Text style={styles.appName}>AgriX</Text>
          <Text style={styles.description}>{desc}</Text>

          <AnimatedButton
            variant="secondary"
            size="large"
            style={styles.button}
            onPress={() => navigation.navigate('Signup')}
          >
            Sign Up
          </AnimatedButton>

          <AnimatedButton
            variant="outline"
            size="large"
            style={styles.button}
            onPress={() => navigation.navigate('Login')}
          >
            Login
          </AnimatedButton>
        </View>

        <View style={styles.featuresRow}>
          <Feature
            icon={require('../assets/icons/smart-farming.png')}
            label="Smart Farming"
            delay={300}
          />
          <Feature
            icon={require('../assets/icons/direct-trade.png')}
            label="Direct Trade"
            delay={400}
          />
          <Feature
            icon={require('../assets/icons/crop-insights.png')}
            label="Crop Insights"
            delay={500}
          />
          <Feature
            icon={require('../assets/icons/expert-advice.png')}
            label="Expert Help"
            delay={600}
          />
        </View>
      </ScrollView>

      <View style={styles.madeWithLove}>
        <Text style={styles.madeWithLoveText}>🇮🇳 Made in India with ❤️</Text>
      </View>
    </View>
  );
};

const Feature = ({ icon, label, delay }) => (
  <AnimatedFadeInView delay={delay} animationType="slideUp" style={styles.featureItem}>
    <GlassmorphicCard blurAmount={5} style={styles.featureCard}>
      <Image source={icon} style={styles.featureIcon} />
    </GlassmorphicCard>
    <Text style={styles.featureLabel}>{label}</Text>
  </AnimatedFadeInView>
);

const styles = StyleSheet.create({
  scrollContainer: {
    flexGrow: 1,
    paddingBottom: 40,
  },
  logoContainer: {
    width: '100%',
    alignItems: 'center',
    marginTop: '10%',
  },
  logo: {
    width: 180,
    height: 180,
    resizeMode: 'contain',
    borderRadius: 90, // Circular logo
  },
  contentContainer: {
    marginTop: '5%',
    width: '100%',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  appName: {
    fontSize: theme.fs0,
    fontFamily: theme.font.dark,
    color: theme.primary, // Updated to Primary Green
    marginBottom: 10,
  },
  description: {
    fontSize: theme.fs6,
    fontFamily: theme.font.light,
    color: theme.text2,
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 22,
  },
  button: {
    width: '100%',
    marginBottom: 10,
  },
  featuresRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 30,
    width: '100%',
    paddingHorizontal: 10,
    flexWrap: 'wrap',
  },
  featureItem: {
    alignItems: 'center',
    width: '23%',
  },
  featureCard: {
    padding: 10,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
    backgroundColor: theme.card + '80', // Slightly more opaque
  },
  featureIcon: {
    width: 32,
    height: 32,
  },
  featureLabel: {
    fontSize: 11,
    textAlign: 'center',
    color: theme.text2,
    fontFamily: theme.font.bold,
  },
  madeWithLove: {
    alignItems: 'center',
    paddingVertical: 10,
  },
  madeWithLoveText: {
    fontSize: 13,
    fontFamily: theme.font.light,
    color: theme.text3,
  },
});

export default Welcome;
