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
const protractor_2 = require("protractor");
const protractor_3 = require("protractor");
const django_1 = require("./django");
const protractor_4 = require("protractor");
function expectIf(args) {
    return __awaiter(this, void 0, void 0, function* () {
        yield selectFilters(args.inputsSelected);
        yield expectProducts(...args.productsPresent);
        yield unselectFilters(args.inputsSelected);
    });
}
exports.expectIf = expectIf;
function expectProducts(...productsToBePresent) {
    return __awaiter(this, void 0, void 0, function* () {
        let productsAll = getAllDjangoProducts();
        let productsNotToBePresent = productsAll.filter(product => {
            let isShouldNotBePresent = !productsToBePresent.includes(product);
            return isShouldNotBePresent;
        });
        for (let product of productsAll) {
            let isProductPresent = yield isProductElemPresent(product);
            let isShouldBePresent = productsToBePresent.includes(product);
            if (isShouldBePresent) {
                expect(isProductPresent).toBe(true);
            }
            let isShouldNotBePresent = productsNotToBePresent.includes(product);
            if (isShouldNotBePresent) {
                expect(isProductPresent).toBe(false);
            }
        }
    });
}
exports.expectProducts = expectProducts;
function expectProductsToBeInOrder(productsExpected) {
    return __awaiter(this, void 0, void 0, function* () {
        let productNamesExpected = productsExpected.map(product => product.name);
        let productNamesElems = yield protractor_3.$$(`span.product-name`).getWebElements();
        let productNames = [];
        for (let productNameElem of productNamesElems) {
            let productName = yield productNameElem.getText();
            productNames.push(productName);
        }
        expect(productNames).toEqual(productNamesExpected);
    });
}
exports.expectProductsToBeInOrder = expectProductsToBeInOrder;
function selectFilters(filtersToSelect) {
    return __awaiter(this, void 0, void 0, function* () {
        yield clickOnInputs(filtersToSelect);
    });
}
function unselectFilters(filtersToUnselect) {
    return __awaiter(this, void 0, void 0, function* () {
        yield clickOnInputs(filtersToUnselect);
    });
}
function clickOnInputs(inputs) {
    return __awaiter(this, void 0, void 0, function* () {
        for (let input of inputs) {
            yield input.click();
        }
        yield protractor_4.browser.waitForAngular();
    });
}
function isProductElemPresent(product) {
    return __awaiter(this, void 0, void 0, function* () {
        let productElem = getProductElement(product);
        let isProductElemPresent = yield productElem.isPresent();
        return isProductElemPresent;
    });
}
function getProductElement(product) {
    let selector = protractor_2.by.cssContainingText(`span.product-name`, product.name);
    return protractor_1.element(selector);
}
function getAllDjangoProducts() {
    let productsAll = [];
    for (let productKey in django_1.products) {
        let product = django_1.products[productKey];
        productsAll.push(product);
    }
    return productsAll;
}
//# sourceMappingURL=matchers.js.map