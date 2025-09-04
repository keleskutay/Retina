import * as ImagePicker from 'expo-image-picker';
import { useState } from 'react';
import { Button, Image, StyleSheet, View } from 'react-native';
import Products from './Products';

type Product = {
  distance: number
  entity: {"product_img": string, "product_url": string}
}

export default function PickImage() {
  const [image, setImage] = useState<string | null>(null);
  const [product, setProduct] = useState<Product[] | null>(null);

  const pickImage = async () => {
    // No permissions request is necessary for launching the image library
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setProduct([])
      setImage(result.assets[0].uri);
    }
  };

  const searchImage = async () => {
    const regex = /data:.*base64,/
    const result = await fetch('http://127.0.0.1:8000/query', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      image_data: image?.replace(regex, ""),
      }),
    })
    .then(response => response.json())
    .then(
      data => setProduct(data["msg"])
    );
    }

  return (
    <View style={styles.container}>
        <Button title="Pick an image" onPress={pickImage} color={styles.button.color}/>
        {image && <Image source={{ uri: image }} style={styles.image} resizeMode='stretch'/>}
        {image && <Button title="Search" onPress={searchImage} color={styles.button.color} />}
        {product && <Products products={product} />}
    </View>
  );
}

const styles = StyleSheet.create({
    container : {
        marginVertical: 20,
    },
    image: {
        width: 300,
        height: 400
    },
    button: {
        color: "#000000ff",
    }
})


