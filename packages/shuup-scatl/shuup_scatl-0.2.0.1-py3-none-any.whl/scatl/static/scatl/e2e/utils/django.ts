/**
 * 0: KAS
 *     price: 1400
 *     attrim
 *         language: english, ukrainian, german
 *         license_num: 1, 5, 6
 *
 * 1: Node 32
 *     price: 1100
 *     attrim
 *         language: english, swedish, bulgarian
 *         license_num: 1, 2, 3
 *
 * 2: Avast
 *     price: 900
 *     attrim
 *         language: english, swedish, ukrainian
 *         license_num: 1, 2, 3, 4, 5, 6
 */


export const BASE_URL = 'http://localhost:8082/catalog'


export enum Sorting {
    NameAZ,
    NameZA,
    PriceMinMax,
    PriceMaxMin,
}


export const products = {
    kas: {name: 'KAS'} as Product,
    nod: {name: 'Node 32'} as Product,
    ava: {name: 'Avast'} as Product,
}


export const inputs = {
    sorting: {
        name: 'sorting',
    } as InputData,
    lang: {
        name: 'language',
        vals: {
            en: 'english',
            sv: 'swedish',
            bg: 'bulgarian',
            de: 'german',
            ua: 'ukrainian',
        },
    } as InputData,
    licenseNum: {
        name: 'license_num',
        vals: {1: `1`, 2: `2`, 3: `3`, 4: `4`, 5: `5`, 6: `6`},
    } as InputData,
    priceMin: {
        name: `price-min`,
    } as InputData,
    priceMax: {
        name: `price-max`,
    } as InputData,
}


export interface InputData {
    name: string
    vals: any
}

export interface Product {
    name: string
}
