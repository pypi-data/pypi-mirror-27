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
const utils_1 = require("./utils/utils");
const django_1 = require("./utils/django");
const django_2 = require("./utils/django");
const django_3 = require("./utils/django");
describe('control form price range', () => {
    beforeAll((done) => __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.browser.get(django_3.BASE_URL);
        done();
    }));
    it('filters by max price', (done) => __awaiter(this, void 0, void 0, function* () {
        yield utils_1.setPriceInput(django_1.inputs.priceMin, 0);
        yield utils_1.setPriceInput(django_1.inputs.priceMax, 1000);
        yield matchers_1.expectProducts(django_2.products.ava);
        done();
    }));
    it('filters by min price', (done) => __awaiter(this, void 0, void 0, function* () {
        yield utils_1.setPriceInput(django_1.inputs.priceMin, 1200);
        yield utils_1.setPriceInput(django_1.inputs.priceMax, 10000);
        yield matchers_1.expectProducts(django_2.products.kas);
        done();
    }));
    it('filters by min and max price', (done) => __awaiter(this, void 0, void 0, function* () {
        yield utils_1.setPriceInput(django_1.inputs.priceMin, 1000);
        yield utils_1.setPriceInput(django_1.inputs.priceMax, 1300);
        yield matchers_1.expectProducts(django_2.products.nod);
        done();
    }));
});
//# sourceMappingURL=price-range-form.comp.e2e-spec.js.map