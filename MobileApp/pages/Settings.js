import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  StatusBar,
} from 'react-native';
import { theme } from '../theme.config';
import { useNavigation } from '@react-navigation/native';
import { AnimatedCircularProgress } from 'react-native-circular-progress';
import Header from '../components/Header';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../context/UserContext';
import { BACKEND_URL } from '../backendConfig';
import Toast from 'react-native-toast-message';
import { useTranslation } from 'react-i18next';
import GlassmorphicCard from '../components/GlassmorphicCard';
import Icon from 'react-native-vector-icons/Ionicons';
import AnimatedButton from '../components/AnimatedButton';

const Settings = () => {
  const navigation = useNavigation();
  const { user, logout } = useContext(UserContext);
  const [progress, setProgress] = useState(0);
  const { t } = useTranslation();

  const btnList = [
    { name: t('update_profile'), route: 'UpdateProfile', icon: 'person-outline' },
    { name: t('document'), route: 'Documents', icon: 'document-text-outline' },
    { name: t('change_language'), route: 'LanguageChange', icon: 'language-outline' },
    { name: t('change_password'), route: 'PasswordChange', icon: 'lock-closed-outline' },
  ];

  useEffect(() => {
    const fetchProfileCompletion = async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/auth/profile-completion`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        });
        const data = await res.json();
        console.log('res', data)
        if (data.success) {
          setProgress(data.percentage);
        } else {
          setProgress(0);
          Toast.show({
            type: 'error',
            text1: 'Error occured while fetching profile data',
            text2: data.message,
          });
        }
      } catch (err) {
        console.log(err);
        Toast.show({
          type: 'error',
          text1: 'Error occured while fetching profile data',
          text2: err.toString(),
        });
      }
    };
    fetchProfileCompletion();
  }, []);

  const handleLogout = async () => {
    try {
      const result = await logout();
      if (result.success) {
        Toast.show({
          type: 'success',
          text1: 'Logout',
          text2: result.message,
        });
        navigation.navigate('Welcome');
      } else {
        Toast.show({
          type: 'error',
          text1: 'Logout error',
          text2: result.message,
        });
      }
    } catch (err) {
      Toast.show({
        type: 'error',
        text1: 'Logout error',
        text2: err,
      });
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: theme.bg }}>
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
          backgroundColor: theme.accent + '10',
          borderRadius: 125,
        }}
      />

      <Header text={t('settings')} />

      <ScrollView contentContainerStyle={{ padding: 20, paddingBottom: 100 }}>

        {/* Profile Completion Card */}
        <GlassmorphicCard style={styles.progressCard} blurAmount={10}>
          <View style={styles.progressRow}>
            <AnimatedCircularProgress
              size={70}
              width={6}
              fill={progress}
              tintColor={theme.secondary}
              backgroundColor={theme.border}
              lineCap="round"
              duration={1000}>
              {() => (
                <Text style={styles.progressText}>{Math.round(progress)}%</Text>
              )}
            </AnimatedCircularProgress>
            <View style={styles.progressInfo}>
              <Text style={styles.progressTitle}>Profile Status</Text>
              <Text style={styles.progressDesc}>{t('profile_complete', { progress })}</Text>
            </View>
          </View>
        </GlassmorphicCard>

        {/* Menu Options */}
        <View style={styles.menuContainer}>
          {btnList.map((item, index) => (
            <GlassmorphicCard key={index} style={styles.menuItemCard} blurAmount={5}>
              <TouchableOpacity
                style={styles.menuItem}
                onPress={() => {
                  if (item.route) navigation.navigate(item.route);
                }}>
                <View style={styles.menuIconContainer}>
                  <Icon name={item.icon || 'chevron-forward-outline'} size={20} color={theme.primary} />
                </View>
                <Text style={styles.menuText}>{item.name}</Text>
                <Icon name="chevron-forward" size={18} color={theme.text3} />
              </TouchableOpacity>
            </GlassmorphicCard>
          ))}

          <AnimatedButton style={styles.logoutButton} onPress={handleLogout} variant="primary">
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
              <Text style={styles.logoutText}>{t('logout')}</Text>
              <Icon name="log-out-outline" size={18} color={theme.white} />
            </View>
          </AnimatedButton>
        </View>

      </ScrollView>
    </View>
  );
};
export default Settings;

const styles = StyleSheet.create({
  progressCard: {
    padding: 20,
    marginBottom: 25,
    backgroundColor: 'rgba(255,255,255,0.7)',
  },
  progressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 20,
  },
  progressText: {
    fontSize: 14,
    color: theme.text,
    fontFamily: theme.font.bold,
  },
  progressInfo: {
    flex: 1,
  },
  progressTitle: {
    fontSize: theme.fs5,
    fontFamily: theme.font.bold,
    color: theme.text,
    marginBottom: 5,
  },
  progressDesc: {
    fontSize: 13,
    color: theme.text2,
    fontFamily: theme.font.regular,
    lineHeight: 18,
  },
  menuContainer: {
    gap: 12,
  },
  menuItemCard: {
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.6)',
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  menuIconContainer: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: theme.primary + '15',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
  },
  menuText: {
    fontSize: theme.fs6,
    color: theme.text,
    fontFamily: theme.font.bold,
    flex: 1,
  },
  logoutButton: {
    marginTop: 20,
    backgroundColor: theme.danger,
    width: '100%',
  },
  logoutText: {
    color: 'white',
    fontFamily: theme.font.bold,
    fontSize: theme.fs6,
  },
});
