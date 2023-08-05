import {URLSearchParams} from '@angular/http'

import {QueryData} from 'app/shared/query-data/query-data.model'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {AttrimOptionValue} from 'app/shared/query-data/query-data.model'
import {Sorting} from 'app/shared/query-data/query-data.model'
import {Injectable} from '@angular/core'


@Injectable()
export class QueryDataToURLSearchParamsSerializer {
    private params: URLSearchParams

    toSearchParams(queryData: QueryData): URLSearchParams {
        this.params = new URLSearchParams()
        this.addAttrimClassesToParams(queryData)
        this.addPriceRangeToParams(queryData)
        this.addCategoryToParams(queryData)
        this.addSortingToParams(queryData)
        this.addPageToParams(queryData)
        return this.params
    }

    private addAttrimClassesToParams(queryData: QueryData) {
        for (let cls of queryData.attrimClsArray) {
            let optionsSelected: AttrimOption[] = cls.options.filter(
                option => option.isSelected === true
            )
            if (optionsSelected.length === 0) {
                continue
            }
            let optionValuesList: AttrimOptionValue[] = optionsSelected.map(
                option => option.value
            )
            let optionValues: string = optionValuesList.join(',')
            this.params.set(`filter[attrim.${cls.code}]`, optionValues)
        }
    }

    private addPriceRangeToParams(queryData: QueryData) {
        let range = queryData.priceRange!!
        this.params.set(`filter[price]`, `${range.min},${range.max}`)
    }

    private addCategoryToParams(queryData: QueryData) {
        if (queryData.categorySlug) {
            this.params.set('filter[category]', queryData.categorySlug)
        }
    }

    private addSortingToParams(queryData: QueryData) {
        switch (queryData.sorting) {
            case Sorting.NameAZ:
                this.params.set('sort', 'name')
                break
            case Sorting.NameZA:
                this.params.set('sort', '-name')
                break
            case Sorting.PriceMinMax:
                this.params.set('sort', 'price')
                break
            case Sorting.PriceMaxMin:
                this.params.set('sort', '-price')
                break
        }
    }

    private addPageToParams(queryData: QueryData) {
        this.params.set(`page`, String(queryData.pageCurrent))
    }
}
