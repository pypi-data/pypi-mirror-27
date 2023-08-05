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
const utils_1 = require("./utils/utils");
const django_3 = require("./utils/django");
const protractor_2 = require("protractor");
describe('control-form attrim', () => {
    beforeAll((done) => __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.browser.get(django_2.BASE_URL);
        done();
    }));
    it('filters by language', (done) => __awaiter(this, void 0, void 0, function* () {
        yield matchers_1.expectIf({
            inputsSelected: [utils_1.getInputElem(django_3.inputs.lang, django_3.inputs.lang.vals.sv)],
            productsPresent: [django_1.products.nod, django_1.products.ava],
        });
        yield matchers_1.expectIf({
            inputsSelected: [utils_1.getInputElem(django_3.inputs.lang, django_3.inputs.lang.vals.bg)],
            productsPresent: [django_1.products.nod],
        });
        yield matchers_1.expectIf({
            inputsSelected: [utils_1.getInputElem(django_3.inputs.lang, django_3.inputs.lang.vals.en)],
            productsPresent: [django_1.products.kas, django_1.products.nod, django_1.products.ava],
        });
        yield matchers_1.expectIf({
            inputsSelected: [utils_1.getInputElem(django_3.inputs.lang, django_3.inputs.lang.vals.ua)],
            productsPresent: [django_1.products.kas, django_1.products.ava],
        });
        done();
    }));
    it('filters by license_num', (done) => __awaiter(this, void 0, void 0, function* () {
        yield matchers_1.expectIf({
            inputsSelected: [utils_1.getInputElem(django_3.inputs.licenseNum, django_3.inputs.licenseNum.vals[1])],
            productsPresent: [django_1.products.kas, django_1.products.nod, django_1.products.ava],
        });
        yield matchers_1.expectIf({
            inputsSelected: [utils_1.getInputElem(django_3.inputs.licenseNum, django_3.inputs.licenseNum.vals[2])],
            productsPresent: [django_1.products.nod, django_1.products.ava],
        });
        done();
    }));
    it('filters by language and license_num', (done) => __awaiter(this, void 0, void 0, function* () {
        yield matchers_1.expectIf({
            inputsSelected: [
                utils_1.getInputElem(django_3.inputs.licenseNum, django_3.inputs.licenseNum.vals[3]),
                utils_1.getInputElem(django_3.inputs.lang, django_3.inputs.lang.vals.bg),
            ],
            productsPresent: [django_1.products.nod],
        });
        yield matchers_1.expectIf({
            inputsSelected: [
                utils_1.getInputElem(django_3.inputs.licenseNum, django_3.inputs.licenseNum.vals[6]),
                utils_1.getInputElem(django_3.inputs.lang, django_3.inputs.lang.vals.ua),
            ],
            productsPresent: [django_1.products.kas, django_1.products.ava],
        });
        done();
    }));
    it('on loading shows the loading bar', (done) => __awaiter(this, void 0, void 0, function* () {
        let loadingBarElem = yield protractor_2.$('.slim-loading-bar-progress').getWebElement();
        yield expectToBeInvisible(loadingBarElem);
        yield utils_1.getInputElem(django_3.inputs.licenseNum, django_3.inputs.licenseNum.vals[1]).click();
        yield expectToBeVisible(loadingBarElem);
        yield protractor_1.browser.waitForAngular();
        yield expectToBeInvisible(loadingBarElem);
        done();
    }));
    function expectToBeInvisible(element) {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.wait(() => __awaiter(this, void 0, void 0, function* () {
                let opacity = yield element.getCssValue('opacity');
                return opacity === '0';
            }));
            expect(yield element.getCssValue('opacity')).toBe('0');
        });
    }
    function expectToBeVisible(element) {
        return __awaiter(this, void 0, void 0, function* () {
            yield protractor_1.browser.wait(() => __awaiter(this, void 0, void 0, function* () {
                let opacity = yield element.getCssValue('opacity');
                return opacity === '1';
            }));
            expect(yield element.getCssValue('opacity')).toBe('1');
        });
    }
});
//# sourceMappingURL=attrim-form.comp.e2e-spec.js.map