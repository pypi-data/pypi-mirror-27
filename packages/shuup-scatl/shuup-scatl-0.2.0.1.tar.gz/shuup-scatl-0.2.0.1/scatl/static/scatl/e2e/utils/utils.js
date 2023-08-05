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
function selectInput(inputData, value) {
    return __awaiter(this, void 0, void 0, function* () {
        yield getInputElem(inputData, value).click();
        yield protractor_3.browser.waitForAngular();
    });
}
exports.selectInput = selectInput;
function setPriceInput(inputData, value) {
    return __awaiter(this, void 0, void 0, function* () {
        yield setNumberInput(inputData.name, value);
        yield protractor_3.browser.waitForAngular();
    });
}
exports.setPriceInput = setPriceInput;
function getInputElem(inputData, value) {
    return protractor_1.$(`[name='${inputData.name}'][value='${value}']`);
}
exports.getInputElem = getInputElem;
/** Because protractor 5.1.2 can't handle number inputs as usual. */
function setNumberInput(name, value) {
    return __awaiter(this, void 0, void 0, function* () {
        var input = protractor_1.$(`input[name='${name}']`);
        yield clearInputAndSetValue(input, value);
        yield triggerNativeOnchange();
    });
}
function clearInputAndSetValue(input, value) {
    return __awaiter(this, void 0, void 0, function* () {
        yield input.sendKeys(protractor_2.protractor.Key.chord(protractor_2.protractor.Key.CONTROL, 'a'));
        yield input.sendKeys(String(value));
    });
}
function triggerNativeOnchange() {
    return __awaiter(this, void 0, void 0, function* () {
        yield resetFocus();
    });
}
// TODO refactor
/**
 * Trigger `onchange` by removing focus with selecting and unselecting.
 * AFAIK no other way at protractor 5.1.2.
 */
function resetFocus() {
    return __awaiter(this, void 0, void 0, function* () {
        yield protractor_1.$(`[name='language'][value='swedish']`).click();
        yield protractor_1.$(`[name='language'][value='swedish']`).click();
    });
}
//# sourceMappingURL=utils.js.map