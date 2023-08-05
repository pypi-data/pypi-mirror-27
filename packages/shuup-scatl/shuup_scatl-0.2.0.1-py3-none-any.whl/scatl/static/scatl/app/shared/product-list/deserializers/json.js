"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function deserializeProductList(response) {
    let productList = [];
    let productListRaw = response.json().results;
    for (let productRaw of productListRaw) {
        let product = {
            // TODO translation
            name: productRaw.translations.en.name,
            url: productRaw.url,
            price: productRaw.price,
            imageUrl: productRaw.primary_image_url,
        };
        productList.push(product);
    }
    return productList;
}
exports.deserializeProductList = deserializeProductList;
//# sourceMappingURL=json.js.map