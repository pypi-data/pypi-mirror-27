import {browser} from 'protractor'
import {expectIf} from './utils/matchers'
import {products} from './utils/django'
import {BASE_URL} from './utils/django'
import {getInputElem} from './utils/utils'
import {inputs} from './utils/django'
import {$} from 'protractor'
import {WebElement} from 'selenium-webdriver'


describe('control-form attrim', () => {
    beforeAll(async done => {
        await browser.get(BASE_URL)
        done()
    })

    it('filters by language', async done => {
        await expectIf({
            inputsSelected: [getInputElem(inputs.lang, inputs.lang.vals.sv)],
            productsPresent: [products.nod, products.ava],
        })
        await expectIf({
            inputsSelected: [getInputElem(inputs.lang, inputs.lang.vals.bg)],
            productsPresent: [products.nod],
        })
        await expectIf({
            inputsSelected: [getInputElem(inputs.lang, inputs.lang.vals.en)],
            productsPresent: [products.kas, products.nod, products.ava],
        })
        await expectIf({
            inputsSelected: [getInputElem(inputs.lang, inputs.lang.vals.ua)],
            productsPresent: [products.kas, products.ava],
        })
        done()
    })

    it('filters by license_num', async done => {
        await expectIf({
            inputsSelected: [getInputElem(inputs.licenseNum, inputs.licenseNum.vals[1])],
            productsPresent: [products.kas, products.nod, products.ava],
        })
        await expectIf({
            inputsSelected: [getInputElem(inputs.licenseNum, inputs.licenseNum.vals[2])],
            productsPresent: [products.nod, products.ava],
        })
        done()
    })

    it('filters by language and license_num', async done => {
        await expectIf({
            inputsSelected: [
                getInputElem(inputs.licenseNum, inputs.licenseNum.vals[3]),
                getInputElem(inputs.lang, inputs.lang.vals.bg),
            ],
            productsPresent: [products.nod],
        })
        await expectIf({
            inputsSelected: [
                getInputElem(inputs.licenseNum, inputs.licenseNum.vals[6]),
                getInputElem(inputs.lang, inputs.lang.vals.ua),
            ],
            productsPresent: [products.kas, products.ava],
        })
        done()
    })
    
    
    it('on loading shows the loading bar', async done => {
        let loadingBarElem: WebElement = await $('.slim-loading-bar-progress').getWebElement()
        await expectToBeInvisible(loadingBarElem)
        
        await getInputElem(inputs.licenseNum, inputs.licenseNum.vals[1]).click()
        await expectToBeVisible(loadingBarElem)
        
        await browser.waitForAngular()
        await expectToBeInvisible(loadingBarElem)
        
        done()
    })
    
    async function expectToBeInvisible(element: WebElement) {
        await browser.wait(async (): Promise<boolean> => {
            let opacity = await element.getCssValue('opacity')
            return opacity === '0'
        })
        expect(await element.getCssValue('opacity')).toBe('0')
    }
    
    async function expectToBeVisible(element: WebElement) {
        await browser.wait(async (): Promise<boolean> => {
            let opacity = await element.getCssValue('opacity')
            return opacity === '1'
        })
        expect(await element.getCssValue('opacity')).toBe('1')
    }
})
