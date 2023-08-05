import {browser} from 'protractor'
import {expectProducts} from './utils/matchers'
import {setPriceInput} from './utils/utils'
import {inputs} from './utils/django'
import {products} from './utils/django'
import {BASE_URL} from './utils/django'


describe('control form price range', () => {
    beforeAll(async done => {
        await browser.get(BASE_URL)
        done()
    })

    it('filters by max price', async done => {
        await setPriceInput(inputs.priceMin, 0)
        await setPriceInput(inputs.priceMax, 1000)
        await expectProducts(products.ava)
        done()
    })

    it('filters by min price', async done => {
        await setPriceInput(inputs.priceMin, 1200)
        await setPriceInput(inputs.priceMax, 10000)
        await expectProducts(products.kas)
        done()
    })

    it('filters by min and max price', async done => {
        await setPriceInput(inputs.priceMin, 1000)
        await setPriceInput(inputs.priceMax, 1300)
        await expectProducts(products.nod)
        done()
    })
})
