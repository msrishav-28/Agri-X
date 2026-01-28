import React, { useContext } from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  StatusBar,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useTranslation } from 'react-i18next';
import { theme } from '../theme.config';
import { UserContext } from '../context/UserContext';
import GlassmorphicCard from '../components/GlassmorphicCard';

const Profile = () => {
  const { user } = useContext(UserContext);
  const navigation = useNavigation();
  const { t } = useTranslation();

  // Function to render profile picture or initial
  const renderProfilePic = () => {
    if (user?.profilePic) {
      return <Image source={{ uri: user.profilePic }} style={styles.profilePic} />;
    }
    return (
      <View style={[styles.profilePic, styles.profileInitial]}>
        <Text style={styles.profileInitialText}>
          {user?.username ? user.username[0].toUpperCase() : 'U'}
        </Text>
      </View>
    );
  };

  // Helper function to display field value or N/A
  const displayValue = (value) => {
    return value || t('profile.status.notAvailable');
  };

  return (
    <View style={{ flex: 1, backgroundColor: theme.bg }}>
      <StatusBar translucent backgroundColor="transparent" barStyle="dark-content" />
      {/* Background Gradient Orbs */}
      <View
        style={{
          position: 'absolute',
          top: -50,
          right: -100,
          width: 300,
          height: 300,
          backgroundColor: theme.secondary + '15',
          borderRadius: 150,
        }}
      />

      <View style={styles.topNav}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Image
            source={require('../assets/icons/back.png')}
            style={{ width: 25, height: 25, tintColor: 'white' }}
          />
        </TouchableOpacity>
        <Text style={styles.appName}>{t('profile.title')}</Text>
      </View>

      <ScrollView
        contentContainerStyle={[styles.form, { paddingHorizontal: 20 }]}
      >
        <GlassmorphicCard style={styles.headerCard} blurAmount={8}>
          {/* Profile Picture */}
          <View style={styles.profilePicContainer}>
            {renderProfilePic()}
          </View>

          <Text style={styles.usernameText}>{displayValue(user?.username)}</Text>

          <Text style={styles.description}>
            {t('profile.description')}
          </Text>
        </GlassmorphicCard>

        {/* Personal Details */}
        <Text style={styles.sectionTitle}>Personal Details</Text>
        <GlassmorphicCard style={styles.infoCard} blurAmount={5}>
          <InfoRow label={t('profile.fields.role')} value={displayValue(user?.role)} />
          <InfoRow label={t('profile.fields.gender')} value={displayValue(user?.gender)} />
          <InfoRow label={t('profile.fields.bio')} value={displayValue(user?.bio)} />
          <InfoRow label={t('profile.fields.languagesSpoken')} value={user?.languageSpoken?.length > 0 ? user.languageSpoken.join(', ') : t('profile.status.notAvailable')} />
        </GlassmorphicCard>

        {/* Location */}
        <Text style={styles.sectionTitle}>Location</Text>
        <GlassmorphicCard style={styles.infoCard} blurAmount={5}>
          <InfoRow label={t('profile.fields.address')} value={displayValue(user?.location?.address)} />
          <View style={styles.row}>
            <View style={{ flex: 1 }}><InfoRow label={t('profile.fields.city')} value={displayValue(user?.location?.city)} /></View>
            <View style={{ flex: 1 }}><InfoRow label={t('profile.fields.state')} value={displayValue(user?.location?.state)} /></View>
          </View>
          <View style={styles.row}>
            <View style={{ flex: 1 }}><InfoRow label={t('profile.fields.country')} value={displayValue(user?.location?.country)} /></View>
            <View style={{ flex: 1 }}><InfoRow label={t('profile.fields.pincode')} value={displayValue(user?.location?.pincode)} /></View>
          </View>
        </GlassmorphicCard>

        {/* Social & Contact */}
        <Text style={styles.sectionTitle}>Contact & Social</Text>
        <GlassmorphicCard style={styles.infoCard} blurAmount={5}>
          <InfoRow label={t('profile.fields.email')} value={displayValue(user?.email)} />
          <InfoRow label={t('profile.fields.phoneNumber')} value={displayValue(user?.phoneNo)} />
          <InfoRow label={t('profile.fields.facebookUrl')} value={displayValue(user?.socialLinks?.facebook)} />
          <InfoRow label={t('profile.fields.instagramUrl')} value={displayValue(user?.socialLinks?.instagram)} />
        </GlassmorphicCard>

      </ScrollView>
    </View>
  );
};

const InfoRow = ({ label, value }) => (
  <View style={styles.infoRowContainer}>
    <Text style={styles.label}>{label}</Text>
    <Text style={styles.value}>{value}</Text>
  </View>
);

const styles = StyleSheet.create({
  topNav: {
    padding: 16,
    paddingTop: 50,
    flexDirection: 'column',
    backgroundColor: 'transparent',
    gap: 7,
    marginBottom: 0,
  },
  backButton: {
    padding: 10,
    backgroundColor: theme.primary,
    borderRadius: 60,
    justifyContent: 'center',
    alignItems: 'center',
    width: 45,
    height: 45,
    shadowColor: theme.shadow,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 3,
  },
  appName: {
    fontSize: theme.fs0,
    fontFamily: theme.font.dark,
    color: theme.primary,
    marginTop: 10,
  },
  form: {
    paddingBottom: 40,
  },
  headerCard: {
    padding: 20,
    alignItems: 'center',
    marginBottom: 20,
    backgroundColor: theme.primary + '10', // Very light green tint
  },
  infoCard: {
    padding: 15,
    marginBottom: 15,
    backgroundColor: 'rgba(255, 255, 255, 0.65)',
  },
  description: {
    fontSize: theme.fs7,
    fontFamily: theme.font.light,
    color: theme.text2,
    textAlign: 'center',
    marginTop: 5,
  },
  sectionTitle: {
    fontSize: theme.fs6,
    fontFamily: theme.font.bold,
    color: theme.primary,
    marginBottom: 8,
    marginLeft: 4,
  },
  infoRowContainer: {
    marginBottom: 12,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
  },
  label: {
    fontSize: 12,
    fontFamily: theme.font.bold,
    color: theme.text3,
    marginBottom: 2,
    textTransform: 'uppercase',
  },
  value: {
    fontSize: theme.fs6,
    fontFamily: theme.font.regular,
    color: theme.text,
  },
  profilePicContainer: {
    alignItems: 'center',
    marginBottom: 10,
  },
  profilePic: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: theme.border,
    borderWidth: 2,
    borderColor: theme.primary,
  },
  profileInitial: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.bgSecondary,
  },
  profileInitialText: {
    fontSize: 32,
    color: theme.primary,
    fontFamily: theme.font.bold,
  },
  usernameText: {
    fontSize: theme.fs4,
    fontFamily: theme.font.bold,
    color: theme.text,
  },
});

export default Profile;