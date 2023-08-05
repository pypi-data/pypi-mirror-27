import {QueryData} from 'app/shared/query-data/query-data.model'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {AttrimOptionValue} from 'app/shared/query-data/query-data.model'
import {Sorting} from 'app/shared/query-data/query-data.model'
import {Params} from '@angular/router'
import {Injectable} from '@angular/core'


@Injectable()
export class QueryDataToRouteParamsSerializer {
    private params: Params

    toRouteParams(queryData: QueryData): Params {
        this.params = {}
        this.addAttrimClassesToParams(queryData)
        this.addPriceRangeToParams(queryData)
        this.addSortingToParams(queryData)
        this.addPagination(queryData)
        return this.params
    }

    private addAttrimClassesToParams(queryData: QueryData) {
        for (let cls of queryData.attrimClsArray) {
            let optionsSelected: Array<AttrimOption> = cls.options.filter(
                option => option.isSelected === true
            )
            if (optionsSelected.length === 0) {
                continue
            }
            let optionValuesList: Array<AttrimOptionValue> = optionsSelected.map(
                option => option.value
            )
            let optionValues: string = optionValuesList.join('~')
            this.params[`filter.attrim.${cls.code}`] = optionValues
        }
    }

    private addPriceRangeToParams(queryData: QueryData) {
        let range = queryData.priceRange!!
        this.params[`filter.price`] = `${range.min}~${range.max}`
    }

    private addSortingToParams(queryData: QueryData) {
        switch (queryData.sorting) {
            case Sorting.NameAZ:
                this.params['sort'] = 'name'
                break
            case Sorting.NameZA:
                this.params['sort'] = '-name'
                break
            case Sorting.PriceMinMax:
                this.params['sort'] = 'price'
                break
            case Sorting.PriceMaxMin:
                this.params['sort'] = '-price'
                break
        }
    }

    private addPagination(queryData: QueryData) {
        this.params['page'] = queryData.pageCurrent
    }
}
