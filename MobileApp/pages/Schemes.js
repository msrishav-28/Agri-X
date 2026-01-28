import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  Keyboard,
  ActivityIndicator,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/Feather';
import axios from 'axios';
import Markdown from 'react-native-markdown-display';
import Header from '../components/Header';
import { theme } from '../theme.config';
import { AIBACKEND_URL } from '../backendConfig';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useTranslation } from 'react-i18next';
import VoicePlayer from '../components/VoicePlayer';

const API_URL = `${AIBACKEND_URL}/govscheme`;

const Schemes = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lang, setLang] = useState(null);
  const scrollViewRef = useRef();
  const { t, i18n } = useTranslation();

  useEffect(() => {
    const loadLanguage = async () => {
      const storedLang = await AsyncStorage.getItem('appLanguage');
      console.log('Schemes page', storedLang);
      if (storedLang) {
        setLang(storedLang);
        const storedLangVal = await AsyncStorage.getItem('appLanguageValue');
        i18n.changeLanguage(storedLangVal);
      }
    };

    loadLanguage();
  }, []);

  useEffect(() => {
    setMessages([{ from: 'bot', text: t('schemes.botGreeting') }]);
  }, [t, i18n.language]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { from: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    Keyboard.dismiss();
    setLoading(true);
    try {
      const currentLang = i18n.language || lang;
      const query = `${userMsg.text} + please answer in ${currentLang}`;
      const res = await axios.post(API_URL, { query });
      let botText = res.data?.response || t('schemes.error.noData');
      setMessages(prev => [
        ...prev,
        { from: 'bot', text: botText, fromBackend: true },
      ]); // Add fromBackend flag
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { from: 'bot', text: t('schemes.error.network'), fromBackend: true },
      ]);
    }
    setLoading(false);
  };

  return (
    <View style={theme.container}>
      <StatusBar translucent backgroundColor="transparent" barStyle="dark-content" />

      {/* Background Orbs */}
      <View style={{
        position: 'absolute',
        top: -100,
        right: -100,
        width: 300,
        height: 300,
        borderRadius: 150,
        backgroundColor: theme.secondary,
        opacity: 0.1,
      }} />
      <View style={{
        position: 'absolute',
        top: 300,
        left: -150,
        width: 400,
        height: 400,
        borderRadius: 200,
        backgroundColor: theme.primary,
        opacity: 0.1,
      }} />

      <Header text={t('schemes.header')} />
      <ScrollView
        ref={scrollViewRef}
        style={styles.chat}
        contentContainerStyle={{ padding: 16, paddingBottom: 50 }}
        onContentSizeChange={() =>
          scrollViewRef.current?.scrollToEnd({ animated: true })
        }>
        {messages.map((msg, idx) => (
          <View
            key={idx}
            style={msg.from === 'user' ? styles.userBubble : styles.botBubble}>
            {msg.from === 'bot' && msg.fromBackend && (
              <VoicePlayer text={msg.text} lang={lang} />
            )}
            <Markdown style={msg.from === 'user' ? markdownUser : markdownBot}>
              {msg.text}
            </Markdown>
          </View>
        ))}
        {loading && (
          <View style={styles.botBubble}>
            <ActivityIndicator size="small" color={theme.primary} />
          </View>
        )}
      </ScrollView>
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder={t('schemes.inputPlaceholder')}
          placeholderTextColor={theme.text3}
          onSubmitEditing={sendMessage}
          editable={!loading}
        />
        <TouchableOpacity
          style={styles.sendBtn}
          onPress={sendMessage}
          disabled={loading}>
          <Icon name="send" size={20} color="white" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.bg },
  chat: { flex: 1, zIndex: 1 },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: theme.primary,
    borderRadius: 12,
    marginBottom: 8,
    padding: 12,
    maxWidth: '85%',
    shadowColor: theme.shadow,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  botBubble: {
    alignSelf: 'flex-start',
    backgroundColor: theme.white,
    borderRadius: 12,
    marginBottom: 8,
    padding: 12,
    maxWidth: '100%',
    borderColor: 'rgba(0,0,0,0.05)',
    borderWidth: 1,
    shadowColor: theme.shadow,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  inputRow: {
    flexDirection: 'row',
    backgroundColor: 'transparent',
    paddingVertical: 10,
    paddingHorizontal: 16,
    alignItems: 'center',
  },
  input: {
    flex: 1,
    borderRadius: 25,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginRight: 10,
    fontSize: theme.fs6,
    color: theme.text,
    fontFamily: theme.font.regular,
    backgroundColor: theme.white,
    borderWidth: 1,
    borderColor: theme.border,
    shadowColor: theme.shadow,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  sendBtn: {
    backgroundColor: theme.primary,
    borderRadius: 25,
    width: 46,
    height: 46,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: theme.primary,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 3,
  },
  sendText: {
    fontFamily: theme.font.bold,
    color: 'white',
    fontSize: 12,
  },
});

const markdownBot = {
  body: { color: theme.text, fontSize: 14, fontFamily: theme.font.regular, lineHeight: 22 },
  strong: { fontFamily: theme.font.bold, color: theme.primary },
  table: { borderWidth: 1, borderColor: theme.border, borderRadius: 8, overflow: 'hidden', marginTop: 8 },
  th: { backgroundColor: theme.bgSecondary, fontFamily: theme.font.bold, color: theme.primary, padding: 8 },
  tr: { borderBottomWidth: 1, borderColor: theme.border },
  td: { padding: 8, color: theme.text2 },
};

const markdownUser = {
  body: { color: theme.white, fontSize: 13, fontFamily: theme.font.regular },
};

export default Schemes;
