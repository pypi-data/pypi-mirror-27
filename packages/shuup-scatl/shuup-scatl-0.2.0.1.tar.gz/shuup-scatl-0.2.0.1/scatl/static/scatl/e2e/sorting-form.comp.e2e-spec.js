"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
const matchers_1 = require("./utils/matchers");
const django_1 = require("./utils/django");
const django_2 = require("./utils/django");
const django_3 = require("./utils/django");
const django_4 = require("./utils/django");
const utils_1 = require("./utils/utils");
describe('control-form sorting', () => {
    let self = {
        productNamesAZ: [
            django_3.products.ava,
            django_3.products.kas,
            django_3.products.nod,
        ],
        productNamesPriceMinMax: [
            django_3.products.ava,
            django_3.products.nod,
            django_3.products.kas,
        ],
    };
    beforeAll((done) => __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.browser.get(django_2.BASE_URL);
        done();
    }));
    it('sorts by default with NameAZ', (done) => __awaiter(this, void 0, void 0, function* () {
        yield matchers_1.expectProductsToBeInOrder(self.productNamesAZ);
        done();
    }));
    it('sorts by NameZA', (done) => __awaiter(this, void 0, void 0, function* () {
        yield utils_1.selectInput(django_4.inputs.sorting, django_1.Sorting.NameZA);
        let productNamesZA = self.productNamesAZ.reverse();
        yield matchers_1.expectProductsToBeInOrder(productNamesZA);
        done();
    }));
    it('sorts by price from min to max', (done) => __awaiter(this, void 0, void 0, function* () {
        yield utils_1.selectInput(django_4.inputs.sorting, django_1.Sorting.PriceMinMax);
        yield matchers_1.expectProductsToBeInOrder(self.productNamesPriceMinMax);
        done();
    }));
    it('sorts by price from max to min', (done) => __awaiter(this, void 0, void 0, function* () {
        yield utils_1.selectInput(django_4.inputs.sorting, django_1.Sorting.PriceMaxMin);
        let productNamesPriceMaxMin = self.productNamesPriceMinMax.reverse();
        yield matchers_1.expectProductsToBeInOrder(productNamesPriceMaxMin);
        done();
    }));
});
//# sourceMappingURL=sorting-form.comp.e2e-spec.js.map