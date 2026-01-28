import React, { useContext, useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Image,
  ScrollView,
} from 'react-native';
import { ActivityIndicator, RadioButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import Toast from 'react-native-toast-message';
import DropDownPicker from 'react-native-dropdown-picker';
import { theme } from '../theme.config';
import { UserContext } from '../context/UserContext';
import AnimatedButton from '../components/AnimatedButton';
import GlassmorphicCard from '../components/GlassmorphicCard';

const Login = () => {
  const { loginWithPhonePassword, loginWithEmailPassword, loading } =
    useContext(UserContext);
  const navigation = useNavigation();
  const desc = 'Login to access your dashboard and manage your activities.';

  const [loginType, setLoginType] = useState('phone');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const [countryCode, setCountryCode] = useState('+91');
  const [openCountry, setOpenCountry] = useState(false);
  const [countryItems, setCountryItems] = useState([
    { label: '+91', value: '+91' },
    { label: '+1', value: '+1' },
    { label: '+44', value: '+44' },
  ]);

  const handleLogin = async () => {
    if (loginType === 'phone') {
      const fullPhone = `${countryCode}${phone}`;
      if (phone.length != 10) {
        Toast.show({
          type: 'error',
          text1: 'Phone number should be valid',
          text2: 'Please enter a 10 digit valid phone number',
        });
        return;
      }
      if (password.length < 8) {
        Toast.show({
          type: 'error',
          text1: 'Password Format failed',
          text2: 'Password cannot be less than 8 characters',
        });
        return;
      }
      const loginData = {
        phoneNo: fullPhone,
        password,
      };
      try {
        const result = await loginWithPhonePassword(loginData);
        if (result.success) {
          Toast.show({
            type: 'success',
            text1: result.message,
            text2: 'User has successfully been signed in',
          });
          // navigation.reset({
          //   index: 0,
          //   routes: [{name: 'MainApp'}],
          // });
          navigation.reset({
            index: 0,
            routes: [{ name: 'MainApp' }],
          });
        } else {
          Toast.show({
            type: 'error',
            text1: 'Login Failed',
            text2: result.message || 'An error occurred during login',
          });
        }
      } catch (err) {
        Toast.show({
          type: 'error',
          text1: 'Login Failed',
          text2: err.message || 'An error occurred during login',
        });
      }
    }
    if (loginType === 'email') {
      if (password.length < 8) {
        Toast.show({
          type: 'error',
          text1: 'Password Format failed',
          text2: 'Password cannot be less than 8 characters',
        });
        return;
      }
      const loginData = {
        email,
        password,
      };
      try {
        const result = await loginWithEmailPassword(loginData);
        if (result.success) {
          Toast.show({
            type: 'success',
            text1: result.message,
            text2: 'User has successfully been signed in',
          });
          navigation.reset({
            index: 0,
            routes: [{ name: 'MainApp' }],
          });
        } else {
          Toast.show({
            type: 'error',
            text1: 'Login Failed',
            text2: result.message || 'An error occurred during login',
          });
        }
      } catch (err) {
        Toast.show({
          type: 'error',
          text1: 'Login Failed',
          text2: err.message || 'An error occurred during login',
        });
      }
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: theme.bg }}>
      {/* Background Gradient Orbs */}
      <View
        style={{
          position: 'absolute',
          top: -100,
          left: -50,
          width: 300,
          height: 300,
          backgroundColor: theme.accent + '15',
          borderRadius: 150,
        }}
      />
      <View
        style={{
          position: 'absolute',
          bottom: 50,
          right: -50,
          width: 250,
          height: 250,
          backgroundColor: theme.primary + '10',
          borderRadius: 125,
        }}
      />

      <View style={styles.topNav}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.navigate('Welcome')}>
          <Image
            source={require('../assets/icons/back.png')}
            style={{ width: 25, height: 25, tintColor: 'white' }}
          />
        </TouchableOpacity>
        <Text style={styles.appName}>Login</Text>
      </View>

      <ScrollView
        contentContainerStyle={[styles.form, { paddingHorizontal: 24 }]}>
        <Text style={styles.description}>{desc}</Text>

        <GlassmorphicCard style={styles.cardContainer} blurAmount={10}>
          {/* Radio Button Group */}
          <View style={styles.radioGroup}>
            <TouchableOpacity
              style={[styles.radioOption, loginType === 'phone' && styles.radioActive]}
              onPress={() => setLoginType('phone')}
            >
              <RadioButton
                value="phone"
                status={loginType === 'phone' ? 'checked' : 'unchecked'}
                onPress={() => setLoginType('phone')}
                color={theme.primary}
              />
              <Text style={[styles.radioText, loginType === 'phone' && { color: theme.primary }]}>Phone</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.radioOption, loginType === 'email' && styles.radioActive]}
              onPress={() => setLoginType('email')}
            >
              <RadioButton
                value="email"
                status={loginType === 'email' ? 'checked' : 'unchecked'}
                onPress={() => setLoginType('email')}
                color={theme.primary}
              />
              <Text style={[styles.radioText, loginType === 'email' && { color: theme.primary }]}>Email</Text>
            </TouchableOpacity>
          </View>

          {loginType === 'phone' ? (
            <View style={styles.phoneRow}>
              <View style={{ width: 90, zIndex: openCountry ? 999 : 1 }}>
                <DropDownPicker
                  open={openCountry}
                  value={countryCode}
                  items={countryItems}
                  setOpen={setOpenCountry}
                  setValue={setCountryCode}
                  setItems={setCountryItems}
                  style={styles.dropdown}
                  textStyle={styles.dropdownText}
                  dropDownContainerStyle={styles.dropdownContainer}
                />
              </View>
              <TextInput
                placeholder="Phone Number"
                placeholderTextColor={theme.text3}
                keyboardType="phone-pad"
                style={[styles.input, { flex: 1 }]}
                value={phone}
                onChangeText={setPhone}
                maxLength={10}
              />
            </View>
          ) : (
            <TextInput
              placeholder="Email"
              placeholderTextColor={theme.text3}
              keyboardType="email-address"
              style={styles.input}
              value={email}
              onChangeText={setEmail}
            />
          )}

          <TextInput
            placeholder="Password"
            placeholderTextColor={theme.text3}
            secureTextEntry={!showPassword}
            style={styles.input}
            value={password}
            onChangeText={setPassword}
          />

          <TouchableOpacity
            onPress={() => setShowPassword(!showPassword)}
            style={styles.togglePassword}>
            <Text
              style={{
                color: theme.primary,
                fontFamily: theme.font.bold,
                fontSize: theme.fs6,
              }}>
              {showPassword ? 'Hide' : 'Show'} Password
            </Text>
          </TouchableOpacity>

          <AnimatedButton
            onPress={handleLogin}
            variant="secondary"
            size="large"
            style={{ marginTop: 10 }}
          >
            {loading ? (
              <ActivityIndicator color="white" />
            ) : (
              'Login'
            )}
          </AnimatedButton>
        </GlassmorphicCard>

      </ScrollView>

      <View style={{ padding: 20 }}>
        <View style={styles.loginLink}>
          <Text style={styles.footer}>Don't have an account?</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Signup')}>
            <Text style={[styles.footer, { color: theme.primary, fontFamily: theme.font.bold }]}>
              {' '}
              Sign Up
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

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
    paddingTop: 10,
  },
  cardContainer: {
    padding: 20,
    backgroundColor: 'rgba(255,255,255,0.7)',
  },
  description: {
    fontSize: theme.fs7,
    fontFamily: theme.font.light,
    color: theme.text2,
    marginBottom: 20,
  },
  footer: {
    fontSize: theme.fs6,
    fontFamily: theme.font.light,
    color: theme.text2,
  },
  input: {
    borderWidth: 1,
    borderColor: theme.border,
    borderRadius: 6,
    padding: 14,
    marginVertical: 8,
    fontSize: theme.fs6,
    backgroundColor: 'rgba(255,255,255,0.6)',
    color: theme.text,
    fontFamily: theme.font.regular,
  },
  togglePassword: {
    marginTop: -4,
    marginBottom: 10,
    alignSelf: 'flex-end',
  },
  loginLink: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    paddingTop: 10,
  },
  radioGroup: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginVertical: 15,
    backgroundColor: theme.bgSecondary,
    borderRadius: 8,
    padding: 5,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 6,
  },
  radioActive: {
    backgroundColor: '#fff',
    shadowColor: theme.shadow,
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  radioText: {
    fontSize: theme.fs6,
    fontFamily: theme.font.bold,
    color: theme.text2,
  },
  phoneRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
    zIndex: 10,
    gap: 10,
  },
  dropdown: {
    borderColor: theme.border,
    borderRadius: 6,
    minHeight: 52,
  },
  dropdownText: {
    fontSize: theme.fs6,
    fontFamily: theme.font.bold,
    color: theme.text,
  },
  dropdownContainer: {
    borderColor: theme.border,
  },
});

export default Login;
