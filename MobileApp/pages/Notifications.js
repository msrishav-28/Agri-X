import { View, Text, StatusBar } from "react-native"
import { theme } from "../theme.config";
import Header from "../components/Header";
import GlassmorphicCard from "../components/GlassmorphicCard";

const Notifications = () => {
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
            <Header text={'Notifications'} />
            <GlassmorphicCard style={{ margin: 24, padding: 20, alignItems: 'center' }} blurAmount={5}>
                <Text style={{ fontFamily: theme.font.regular, color: theme.text2, fontSize: theme.fs6 }}>
                    No new notifications
                </Text>
            </GlassmorphicCard>
        </View>
    )
}
export default Notifications;