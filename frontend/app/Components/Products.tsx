import { FlatList, Image, Linking, ListRenderItem, StyleSheet, TouchableOpacity } from 'react-native';

type Product = {
  distance: number
  entity: {"product_img": string, "product_url": string}
}

type products = {
    products: Product[] | null
}

export default function Products(props: products) {

    const renderItem: ListRenderItem<Product> = ({ item }) => (
        <TouchableOpacity
          style={styles.card}
          onPress={() => Linking.openURL(item.entity["product_url"])}>
          
          <Image source={{uri: "https://upload.wikimedia.org/wikipedia/commons/1/18/Trendyol_online.png"}} resizeMode="stretch" style={{width:145, height:50}}/>
          <Image source={{ uri: item.entity["product_img"] }} style={styles.image} />
        </TouchableOpacity>
      );

    return (
        <FlatList data={props.products} numColumns={2} renderItem={renderItem} />
    );
}

const styles = StyleSheet.create({
image: {
    flex: 1,
    backgroundColor: '#000',
    marginRight: 5,
    },

card: {
    width: 150,
    height:250, 
    backgroundColor: "#fff",
    borderRadius: 12,
    margin: 5,
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowRadius: 6,
    elevation: 3,
    }
})