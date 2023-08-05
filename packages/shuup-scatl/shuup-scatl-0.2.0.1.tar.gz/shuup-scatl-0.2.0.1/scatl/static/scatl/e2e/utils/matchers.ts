import {element} from 'protractor'
import {by} from 'protractor'
import {ElementFinder} from 'protractor'
import {$$} from 'protractor'
import {Product} from './django'
import {products} from './django'
import {browser} from 'protractor'


type ProductName = string


export async function expectIf(args: {
    inputsSelected: Array<ElementFinder>,
    productsPresent: Array<Product>,
}) {
    await selectFilters(args.inputsSelected)
    await expectProducts(...args.productsPresent)
    await unselectFilters(args.inputsSelected)
}


export async function expectProducts(...productsToBePresent: Array<Product>) {
    let productsAll = getAllDjangoProducts()
    let productsNotToBePresent = productsAll.filter(product => {
        let isShouldNotBePresent: boolean = !productsToBePresent.includes(product)
        return isShouldNotBePresent
    })

    for (let product of productsAll) {
        let isProductPresent = await isProductElemPresent(product)

        let isShouldBePresent = productsToBePresent.includes(product)
        if (isShouldBePresent) {
            expect(isProductPresent).toBe(true)
        }

        let isShouldNotBePresent = productsNotToBePresent.includes(product)
        if (isShouldNotBePresent) {
            expect(isProductPresent).toBe(false)
        }
    }
}


export async function expectProductsToBeInOrder(productsExpected: Array<Product>) {
    let productNamesExpected = productsExpected.map(product => product.name)
    let productNamesElems = await $$(`span.product-name`).getWebElements()
    let productNames: Array<ProductName> = []
    for (let productNameElem of productNamesElems) {
        let productName = await productNameElem!!.getText() as ProductName
        productNames.push(productName)
    }
    expect(productNames).toEqual(productNamesExpected)
}


async function selectFilters(filtersToSelect: Array<ElementFinder>) {
    await clickOnInputs(filtersToSelect)
}


async function unselectFilters(filtersToUnselect: Array<ElementFinder>) {
    await clickOnInputs(filtersToUnselect)
}


async function clickOnInputs(inputs: Array<ElementFinder>) {
    for (let input of inputs) {
        await input.click()
    }
    await browser.waitForAngular()
}


async function isProductElemPresent(product: Product): Promise<boolean> {
    let productElem: ElementFinder = getProductElement(product)
    let isProductElemPresent = await productElem.isPresent()
    return isProductElemPresent
}


function getProductElement(product: Product): ElementFinder {
    let selector = by.cssContainingText(`span.product-name`, product.name)
    return element(selector)
}


function getAllDjangoProducts(): Array<Product> {
    let productsAll: Array<Product> = []
    for (let productKey in products) {
        let product = products[productKey]
        productsAll.push(product)
    }
    return productsAll
}
