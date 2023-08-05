import {$} from 'protractor'
import {protractor, ElementFinder} from 'protractor'
import {Sorting} from './django'
import {InputData} from './django'
import {browser} from 'protractor'


export async function selectInput(inputData: InputData, value: string | Sorting) {
    await getInputElem(inputData, value).click()
    await browser.waitForAngular()
}


export async function setPriceInput(inputData: InputData, value: number) {
    await setNumberInput(inputData.name, value)
    await browser.waitForAngular()
}


export function getInputElem(
    inputData: InputData,
    value: string | Sorting,
): ElementFinder {
    return $(`[name='${inputData.name}'][value='${value}']`)
}


/** Because protractor 5.1.2 can't handle number inputs as usual. */
async function setNumberInput(name: string, value: number) {
    var input = $(`input[name='${name}']`)
    await clearInputAndSetValue(input, value)
    await triggerNativeOnchange()
}


async function clearInputAndSetValue(input: ElementFinder, value: number) {
    await input.sendKeys((protractor.Key as any).chord(protractor.Key.CONTROL, 'a'))
    await input.sendKeys(String(value))
}


async function triggerNativeOnchange() {
    await resetFocus()
}


// TODO refactor
/**
 * Trigger `onchange` by removing focus with selecting and unselecting.
 * AFAIK no other way at protractor 5.1.2.
 */
async function resetFocus() {
    await $(`[name='language'][value='swedish']`).click()
    await $(`[name='language'][value='swedish']`).click()
}
