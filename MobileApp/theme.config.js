import { Dimensions, StatusBar } from 'react-native';

const { width, height } = Dimensions.get('window');

export const theme = {
  // Agri-Tech Green Palette
  primary: '#15803d', // Deep Forest Green - Trust, stability (Primary interactions)
  primaryDark: '#14532d', // Darker forest green for pressed states
  secondary: '#22c55e', // Fresh Emerald - Growth, success, active states
  secondaryDark: '#16a34a', // Darker emerald variation

  // Accents & Earth Tones
  accent: '#d97706', // Golden Harvest (Amber) - Call to Action / Highlights
  accentLight: '#fcd34d', // Soft Sunlight - Background accents
  danger: '#ef4444', // Red for errors (kept standard for semantic meaning)
  warning: '#f97316', // Orange for warnings
  success: '#22c55e', // Matches secondary
  info: '#0ea5e9', // Sky Blue - Information (e.g. weather) - kept as a natural sky tone

  // Background Colors
  bg: '#fbfdfc', // Very subtle mint-white tint
  bgSecondary: '#f0fdf4', // Light green tint for secondary backgrounds
  card: '#ffffff', // Pure white cards
  cardSecondary: '#f8fafc', // Light gray-green for secondary cards

  // Border and UI Elements
  border: '#e2e8f0', // Neutral light border
  borderDark: '#cbd5e1', // Slightly darker border
  shadow: '#334155', // Slate shadow (softer than black)
  overlay: 'rgba(20, 83, 45, 0.2)', // Dark green overlay

  // Special Colors
  gradient: ['#15803d', '#22c55e'], // Green gradient (Forest to Emerald)
  gradientSecondary: ['#F59E0B', '#FCD34D'], // Harvest gradient (Amber)
  blue: '#0ea5e9', // Sky blue for weather/water contexts

  // Text Colors
  text: '#1e293b', // Deep Slate - High contrast reading
  text2: '#475569', // Medium Slate - Secondary info
  text3: '#94a3b8', // Light Slate - Placeholders
  textInverse: '#ffffff', // White
  link: '#15803d', // Link color matches primary
  white: '#ffffff',

  // Legacy/Semantic mapping
  darkBrown: '#3f2e00', // Deep Earth Brown - replaces the old dark slate for specifics
  skin: '#ffedd5', // Soft peach/wheat

  fs0: width * 0.099,
  fs00: width * 0.08,
  fs1: width * 0.07,
  fs2: width * 0.055,
  fs3: width * 0.05,
  fs4: width * 0.045,
  fs5: width * 0.04,
  fs6: width * 0.035,
  fs7: width * 0.03,

  r1: 20,
  r2: 12,
  r3: 6,

  font: {
    regular: 'Poppins-Regular',
    bold: 'Poppins-Bold',
    light: 'Poppins-Light',
    thin: 'Poppins-Thin',
    dark: 'Poppins-Black',
  },

  width,
  height,

  container: {
    backgroundColor: 'white',
    width: width,
    height: height + StatusBar.currentHeight,
    padding: width * 0.02,
    paddingTop: StatusBar.currentHeight + width * 0.06,
    flexDirection: 'column',
    paddingTop: StatusBar.currentHeight + 20,
    padding: 20,
  },

  // Additional modern container variants
  containerPrimary: {
    backgroundColor: '#2563EB',
    width: width,
    height: height + StatusBar.currentHeight,
    padding: width * 0.02,
    paddingTop: StatusBar.currentHeight + width * 0.06,
    flexDirection: 'column',
    paddingTop: StatusBar.currentHeight + 20,
    padding: 20,
  },

  containerSecondary: {
    backgroundColor: '#FAFBFC',
    width: width,
    height: height + StatusBar.currentHeight,
    padding: width * 0.02,
    paddingTop: StatusBar.currentHeight + width * 0.06,
    flexDirection: 'column',
    paddingTop: StatusBar.currentHeight + 20,
    padding: 20,
  },

  test: { borderWidth: 1, borderColor: '#E2E8F0' }, // Updated to use new border color

  button: {
    width: '100%',
    paddingVertical: width * 0.04,
    borderRadius: 12, // Increased border radius for modern look
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: width * 0.05,
    backgroundColor: '#2563EB', // Primary button color
  },

  // Additional button variants
  buttonSecondary: {
    width: '100%',
    paddingVertical: width * 0.04,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: width * 0.05,
    backgroundColor: '#10B981',
  },

  buttonOutline: {
    width: '100%',
    paddingVertical: width * 0.04,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: width * 0.05,
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#2563EB',
  },
};
