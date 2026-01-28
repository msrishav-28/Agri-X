import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  StatusBar,
  FlatList,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useTranslation } from 'react-i18next';
import { theme } from '../theme.config';
import Header from '../components/Header';
import GlassmorphicCard from '../components/GlassmorphicCard';

const Chatbot = () => {
  const navigation = useNavigation();
  const scrollViewRef = useRef(null);
  const { t } = useTranslation();

  const predefinedOptions = [
    { label: t('chatbot.options.governmentSchemes'), screen: 'Scheme' },
    { label: t('chatbot.options.cropCare'), screen: 'Crop Care' },
    { label: t('chatbot.options.accessMarket'), screen: 'Market' },
    { label: t('chatbot.options.settings'), screen: 'Settings' },
    { label: t('chatbot.options.viewProfile'), screen: 'Profile' },
    { label: t('chatbot.options.updateProfile'), screen: 'UpdateProfile' },
  ];

  const [chatHistory, setChatHistory] = useState([
    { type: 'bot', text: t('chatbot.initialMessage'), showOptions: true },
  ]);

  const handleUserSelection = (option) => {
    const userMessage = { type: 'user', text: option.label };
    const botMessage1 = { type: 'bot', text: t('chatbot.loadingMessage') };
    const botMessage2 = { type: 'bot', text: t('chatbot.initialMessage'), showOptions: true };

    setChatHistory((prev) => [...prev, userMessage, botMessage1]);

    setTimeout(() => {
      if (option.screen === 'Settings' || option.screen === 'UpdateProfile' || option.screen === 'Profile') {
        navigation.navigate(option.screen);
      } else {
        navigation.navigate('MainApp', { screen: option.screen });
      }

      // Show next menu again after a short pause
      setTimeout(() => {
        setChatHistory((prev) => [...prev, botMessage2]);
      }, 1000);
    }, 2000);
  };

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [chatHistory]);

  const renderOption = ({ item }) => (
    <TouchableOpacity
      onPress={() => handleUserSelection(item)}
      activeOpacity={0.8}
    >
      <GlassmorphicCard style={styles.optionButton} blurAmount={4}>
        <Text style={styles.optionText}>{item.label}</Text>
      </GlassmorphicCard>
    </TouchableOpacity>
  );

  return (
    <View style={{ flex: 1, backgroundColor: theme.bg }}>
      <StatusBar translucent backgroundColor="transparent" barStyle="dark-content" />
      {/* Background Gradient Orbs */}
      <View
        style={{
          position: 'absolute',
          top: -100,
          left: -50,
          width: 300,
          height: 300,
          backgroundColor: theme.accent + '10',
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

      <Header text={t('chatbot.headerTitle')} />
      <ScrollView
        ref={scrollViewRef}
        contentContainerStyle={styles.chatContainer}
        showsVerticalScrollIndicator={false}
      >
        {chatHistory.map((msg, index) => (
          <View
            key={index}
            style={[
              styles.messageBubble,
              msg.type === 'user' ? styles.userBubble : styles.botBubble,
            ]}
          >
            <Text style={[styles.messageText, msg.type === 'user' && { color: 'white' }]}>{msg.text}</Text>

            {/* If this bot message includes options */}
            {msg.showOptions && (
              <FlatList
                data={predefinedOptions}
                renderItem={renderOption}
                keyExtractor={(item, index) => index.toString()}
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.optionsContainer}
              />
            )}
          </View>
        ))}
      </ScrollView>
    </View>
  );
};

export default Chatbot;

const styles = StyleSheet.create({
  chatContainer: {
    paddingBottom: 20,
    paddingTop: 20,
    paddingHorizontal: 15,
  },
  messageBubble: {
    maxWidth: '85%',
    padding: 14,
    borderRadius: 12,
    marginBottom: 12,
  },
  userBubble: {
    backgroundColor: theme.primary,
    borderBottomRightRadius: 2,
    alignSelf: 'flex-end',
    shadowColor: theme.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 2,
  },
  botBubble: {
    backgroundColor: 'white',
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
    borderWidth: 1,
    borderColor: theme.border,
  },
  messageText: {
    fontSize: theme.fs6,
    fontFamily: theme.font.regular,
    color: theme.text,
    lineHeight: 22,
  },
  optionsContainer: {
    paddingTop: 10,
    paddingBottom: 5,
  },
  optionButton: {
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 8,
    marginRight: 10,
    backgroundColor: 'rgba(255,255,255,0.7)',
  },
  optionText: {
    fontSize: 13,
    fontFamily: theme.font.bold,
    color: theme.primary,
    textAlign: 'center',
  },
});