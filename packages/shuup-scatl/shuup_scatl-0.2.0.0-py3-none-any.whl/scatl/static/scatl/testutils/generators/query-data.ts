import FakerStatic = Faker.FakerStatic
import {QueryData} from 'app/shared/query-data/query-data.model'
import {Sorting} from 'app/shared/query-data/query-data.model'
import {AttrimCls} from 'app/shared/query-data/query-data.model'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {UniqueGenerator} from 'testutils/generators/unique'
import {getSampleFromEnum} from 'testutils/enums'
import {PriceRange} from 'app/shared/query-data/query-data.model'


declare var faker: FakerStatic


export class QueryDataGenerator {
    private fake: FakerStatic
    private uniqueGen: UniqueGenerator

    constructor() {
        this.fake = faker
        this.uniqueGen = new UniqueGenerator()
    }

    data(): QueryData {
        let data = new QueryData({
            attrimClsArray: this.attrimClsArray(),
            priceRange: this.priceRange(),
            sorting: this.sorting(),
            pageCurrent: this.fake.random.number({min: 1, max: 50}),
            pageLast: this.fake.random.number({min: 50, max: 100}),
        })
        return data
    }

    sorting(): Sorting {
        let sortingRandom: Sorting = getSampleFromEnum(Sorting)
        return sortingRandom
    }

    attrimClsArray(amount: number = 5): Array<AttrimCls> {
        let classes = [] as Array<AttrimCls>
        for (let num = 0; num <= amount; num++) {
            classes.push(this.attrimCls())
        }
        return classes
    }

    attrimCls(optionsAmount: number = 5): AttrimCls {
        let code = this.uniqueGen.word()
        let cls = new AttrimCls({
            code: code,
            name: code,
            options: this.attrimOptionArray(optionsAmount),
        })
        return cls
    }

    attrimOptionArray(amount: number = 5): Array<AttrimOption> {
        let options = [] as Array<AttrimOption>
        let uniqueGen = new UniqueGenerator()
        for (let num = 0; num <= amount; num++) {
            let option = this.attrimOption({value: uniqueGen.word()})
            options.push(option)
        }
        return options
    }

    attrimOption(args: {value: string}): AttrimOption {
        let option = new AttrimOption({
            value: args.value,
            isSelected: this.fake.random.boolean(),
        })
        return option
    }

    priceRange(): PriceRange {
        let min: number, max: number
        if (window.DJANGO === undefined) {
            min = this.fake.random.number()
            max = this.fake.random.number({min: min})
        } else {
            min = window.DJANGO.priceRange.min
            max = window.DJANGO.priceRange.max
        }
        let range = new PriceRange(min, max)
        return range
    }
}
