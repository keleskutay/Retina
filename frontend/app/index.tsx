import { ScrollView, StyleSheet, View } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';
import PickImage from "./Components/PickImage";

export default function Index() {

  return (
    <ScrollView>
      <SafeAreaProvider>
        <SafeAreaView edges={['top']}>
          <View style={styles.container}>
              <PickImage/>
          </View>
        </SafeAreaView>
      </SafeAreaProvider>
    </ScrollView>
        
  );
}

const styles = StyleSheet.create({
  container: {
    flex:1,
    flexDirection: "column",
    alignItems: 'center',
  },
});