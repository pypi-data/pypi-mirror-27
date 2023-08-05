import {browser} from 'protractor'
import {expectProducts} from './utils/matchers'
import {BASE_URL} from './utils/django'
import {inputs, products} from './utils/django'
import {Sorting} from './utils/django'
import {selectInput} from './utils/utils'
import {setPriceInput} from './utils/utils'
import {$} from 'protractor'


describe('router', () => {
    let self = {
        params: {
            lang: 'filter.attrim.language=swedish',
            license: 'filter.attrim.license_num=1',
        },
    }

    it('initializes filters from the router params', async done => {
        await browser.get(`${BASE_URL};${self.params.lang};${self.params.license};`)
        await browser.waitForAngular()
        await expectProducts(products.nod, products.ava)
        done()
    })

    it('changes the url according to the selected filters', async done => {
        await browser.get(BASE_URL)

        await selectInput(inputs.licenseNum, inputs.licenseNum.vals[1])
        await selectInput(inputs.lang, inputs.lang.vals.sv)

        let priceMaxNew = 1000
        await setPriceInput(inputs.priceMax, priceMaxNew)

        await selectInput(inputs.sorting, Sorting.NameZA)

        let urlExpected = `${BASE_URL};`
            + `filter.attrim.${inputs.lang.name}=${inputs.lang.vals.sv};`
            + `filter.attrim.${inputs.licenseNum.name}=${inputs.licenseNum.vals[1]};`
            + `filter.price=900~${priceMaxNew};`
            + `sort=-name;`
            + `page=1`
        expect(await browser.getCurrentUrl()).toBe(urlExpected)
        done()
    })
    
    it('shows an error if the url was incorrect', async done => {
        await browser.get(`${BASE_URL};filter.price=900~g1400`)
        await browser.wait(async (): Promise<boolean> => {
            return $(`.simple-notification.error`).isPresent()
        })
        expect(await $(`.simple-notification.error`).isPresent()).toBe(true)
        done()
    })
})
