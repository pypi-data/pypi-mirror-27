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
const utils_1 = require("./utils/utils");
const utils_2 = require("./utils/utils");
const protractor_2 = require("protractor");
describe('router', () => {
    let self = {
        params: {
            lang: 'filter.attrim.language=swedish',
            license: 'filter.attrim.license_num=1',
        },
    };
    it('initializes filters from the router params', (done) => __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.browser.get(`${django_1.BASE_URL};${self.params.lang};${self.params.license};`);
        yield protractor_1.browser.waitForAngular();
        yield matchers_1.expectProducts(django_2.products.nod, django_2.products.ava);
        done();
    }));
    it('changes the url according to the selected filters', (done) => __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.browser.get(django_1.BASE_URL);
        yield utils_1.selectInput(django_2.inputs.licenseNum, django_2.inputs.licenseNum.vals[1]);
        yield utils_1.selectInput(django_2.inputs.lang, django_2.inputs.lang.vals.sv);
        let priceMaxNew = 1000;
        yield utils_2.setPriceInput(django_2.inputs.priceMax, priceMaxNew);
        yield utils_1.selectInput(django_2.inputs.sorting, django_3.Sorting.NameZA);
        let urlExpected = `${django_1.BASE_URL};`
            + `filter.attrim.${django_2.inputs.lang.name}=${django_2.inputs.lang.vals.sv};`
            + `filter.attrim.${django_2.inputs.licenseNum.name}=${django_2.inputs.licenseNum.vals[1]};`
            + `filter.price=900~${priceMaxNew};`
            + `sort=-name;`
            + `page=1`;
        expect(yield protractor_1.browser.getCurrentUrl()).toBe(urlExpected);
        done();
    }));
    it('shows an error if the url was incorrect', (done) => __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.browser.get(`${django_1.BASE_URL};filter.price=900~g1400`);
        yield protractor_1.browser.wait(() => __awaiter(this, void 0, void 0, function* () {
            return protractor_2.$(`.simple-notification.error`).isPresent();
        }));
        expect(yield protractor_2.$(`.simple-notification.error`).isPresent()).toBe(true);
        done();
    }));
});
//# sourceMappingURL=router.e2e-spec.js.map