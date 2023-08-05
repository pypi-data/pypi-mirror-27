"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.BASE_URL = 'http://localhost:8082/catalog';
var Sorting;
(function (Sorting) {
    Sorting[Sorting["NameAZ"] = 0] = "NameAZ";
    Sorting[Sorting["NameZA"] = 1] = "NameZA";
    Sorting[Sorting["PriceMinMax"] = 2] = "PriceMinMax";
    Sorting[Sorting["PriceMaxMin"] = 3] = "PriceMaxMin";
})(Sorting = exports.Sorting || (exports.Sorting = {}));
exports.products = {
    kas: { name: 'KAS' },
    nod: { name: 'Node 32' },
    ava: { name: 'Avast' },
};
exports.inputs = {
    sorting: {
        name: 'sorting',
    },
    lang: {
        name: 'language',
        vals: {
            en: 'english',
            sv: 'swedish',
            bg: 'bulgarian',
            de: 'german',
            ua: 'ukrainian',
        },
    },
    licenseNum: {
        name: 'license_num',
        vals: { 1: `1`, 2: `2`, 3: `3`, 4: `4`, 5: `5`, 6: `6` },
    },
    priceMin: {
        name: `price-min`,
    },
    priceMax: {
        name: `price-max`,
    },
};
//# sourceMappingURL=django.js.map