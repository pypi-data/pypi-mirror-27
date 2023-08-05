import {Response} from '@angular/http'

import {Product} from 'app/shared/product-list/product.model'


export function deserializeProductList(response: Response): Array<Product> {
    let productList: Array<Product> = []
    let productListRaw: Array<any> = response.json().results
    for (let productRaw of productListRaw) {
        let product: Product = {
            // TODO translation
            name: productRaw.translations.en.name,
            url: productRaw.url,
            price: productRaw.price,
            imageUrl: productRaw.primary_image_url,
        }
        productList.push(product)
    }
    return productList
}
