import {browser} from 'protractor'
import {expectProductsToBeInOrder} from './utils/matchers'
import {Sorting} from './utils/django'
import {BASE_URL} from './utils/django'
import {products} from './utils/django'
import {inputs} from './utils/django'
import {Product} from './utils/django'
import {selectInput} from './utils/utils'


describe('control-form sorting', () => {
    let self = {
        productNamesAZ: [
            products.ava,
            products.kas,
            products.nod,
        ] as Array<Product>,
        productNamesPriceMinMax: [
            products.ava,
            products.nod,
            products.kas,
        ] as Array<Product>,
    }

    beforeAll(async done => {
        await browser.get(BASE_URL)
        done()
    })

    it('sorts by default with NameAZ', async done => {
        await expectProductsToBeInOrder(self.productNamesAZ)
        done()
    })

    it('sorts by NameZA', async done => {
        await selectInput(inputs.sorting, Sorting.NameZA)
        let productNamesZA = self.productNamesAZ.reverse()
        await expectProductsToBeInOrder(productNamesZA)
        done()
    })

    it('sorts by price from min to max', async done => {
        await selectInput(inputs.sorting, Sorting.PriceMinMax)
        await expectProductsToBeInOrder(self.productNamesPriceMinMax)
        done()
    })

    it('sorts by price from max to min', async done => {
        await selectInput(inputs.sorting, Sorting.PriceMaxMin)
        let productNamesPriceMaxMin = self.productNamesPriceMinMax.reverse()
        await expectProductsToBeInOrder(productNamesPriceMaxMin)
        done()
    })
})
