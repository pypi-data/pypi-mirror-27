import {ActivatedRouteSnapshot} from '@angular/router'
import {Sorting} from 'app/shared/query-data/query-data.model'
import {AttrimCls} from 'app/shared/query-data/query-data.model'
import {AttrimOption} from 'app/shared/query-data/query-data.model'
import {QueryData} from 'app/shared/query-data/query-data.model'
import {CategorySlug} from 'app/shared/query-data/query-data.model'
import {routeLocation} from 'app/app.routing'
import {PriceRange} from 'app/shared/query-data/query-data.model'
import {PageNum} from 'app/shared/query-data/query-data.model'
import {Injectable} from '@angular/core'


@Injectable()
export class RouteSnapshotToQueryDataDeserializer {
    private routeSnapshot: ActivatedRouteSnapshot
    
    toQueryData(routeSnapshot: ActivatedRouteSnapshot): QueryData {
        this.routeSnapshot = routeSnapshot
        let queryData = new QueryData({
            attrimClsArray: this.deserializeAttrimClsArray(),
            priceRange: this.deserializePriceRange(),
            categorySlug: this.deserializeCategorySlug(),
            sorting: this.deserializeSorting(),
            pageCurrent: this.deserializePageCurrent(),
            pageLast: this.deserializePageLast(),
        })
        return queryData
    }
    
    private deserializeCategorySlug(): CategorySlug | null {
        let routeLocationCurrent = this.routeSnapshot.data[`location`]
        let isUrlContainsCategory = routeLocationCurrent === routeLocation.category
        if (isUrlContainsCategory) {
            let currentUrl = this.getCurrentUrl(this.routeSnapshot)
            let categorySlugMatch = /([\w\-]+)?\/?$/g.exec(currentUrl)
            let isCategorySlugNotFound = categorySlugMatch === null
            if (isCategorySlugNotFound) {
                return null
            }
            let categorySlug = categorySlugMatch!![1]
            return categorySlug
        } else {
            return null
        }
    }

    private deserializeAttrimClsArray(): Array<AttrimCls> {
        let clsArray: Array<AttrimCls> = []
        let regexForClsCode = /filter\.attrim\.(\w+)/i
        for (let paramName in this.routeSnapshot.params) {
            let clsCodeMatch = paramName.match(regexForClsCode)
            if (!clsCodeMatch) {
                // it's ok, the params can contain not only attrim classes
                continue
            }
            let clsCode = clsCodeMatch[1]
            let cls = new AttrimCls({code: clsCode})

            // TODO assert valid string
            let optionValues = this.routeSnapshot.params[paramName].split(`~`)
            for (let optionValue of optionValues) {
                let option = new AttrimOption({
                    value: optionValue,
                    isSelected: true,
                })
                cls.options.push(option)
            }
            clsArray.push(cls)
        }
        return clsArray
    }

    private deserializePriceRange(): PriceRange {
        let params = this.routeSnapshot.params
        for (let paramName in params) {
            let isPriceRangeParam = paramName.indexOf(`filter.price`) !== -1
            if (isPriceRangeParam) {
                let rangeValuesStr: string = params[paramName]
                this.validateRangeValues(rangeValuesStr)
                let rangeValuesRaw: Array<string> = params[paramName].split(`~`)
                let min = Number(rangeValuesRaw[0])
                let max = Number(rangeValuesRaw[1])
                return new PriceRange(min, max)
            }
        }
        return new PriceRange(
            window.DJANGO.priceRange.min,
            window.DJANGO.priceRange.max,
        )
    }

    private deserializeSorting(): Sorting {
        let sortingParamKey = `sort`
        let sortType = this.routeSnapshot.params[sortingParamKey]
        switch (sortType) {
            case `name`:
                return Sorting.NameAZ
            case `-name`:
                return Sorting.NameZA
            case `price`:
                return Sorting.PriceMinMax
            case `-price`:
                return Sorting.PriceMaxMin
            default:
                return Sorting.NameAZ
        }
    }

    private deserializePageCurrent(): PageNum {
        let page: PageNum
        if (`page` in this.routeSnapshot.params) {
            page = Number(this.routeSnapshot.params[`page`])
        } else {
            page = 1
        }
        return page
    }

    private deserializePageLast(): PageNum {
        let pageLast: PageNum
        if (`last` in this.routeSnapshot.params) {
            pageLast = Number(this.routeSnapshot.params[`last`])
        } else {
            pageLast = 1
        }
        return pageLast
    }

    private getCurrentUrl(snapshot: ActivatedRouteSnapshot): string {
        let urlPaths: Array<string> = []
        for (let urlSegment of snapshot.url) {
            urlPaths.push(urlSegment.path)
        }
        let currentUrl = urlPaths.join(`/`)
        return currentUrl
    }
    
    private validateRangeValues(priceRangeValuesRaw: string) {
        let errorMessage = 'Invalid price range parameter'
        let rangeMatch = /^[0-9]+~[0-9]+$/g.exec(priceRangeValuesRaw)
        if (rangeMatch === null) {
            throw Error(errorMessage)
        }
    }
}
