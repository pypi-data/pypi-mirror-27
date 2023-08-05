import {Injectable} from '@angular/core'
import {PageNum} from 'app/shared/query-data/query-data.model'


@Injectable()
export class PageRangeService {
    /**
     * @example
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 20, pageCurrent: 10, range: 3,
     *     }) === [7, 8, 9, 10, 11, 12, 13]
     *
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 20, pageCurrent: 10, range: 2,
     *     }) === [8, 9, 10, 11, 12]
     *
     *     // the start and the end pages aren't included
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 7, pageCurrent: 4, range: 3,
     *     }) === [2, 3, 4, 5, 6]
     *
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 1, pageCurrent: 1, range: 3,
     *     }) === []
     */
    getPageArrayRange(args: {
        pageStart: PageNum, pageEnd: PageNum, pageCurrent: PageNum, range: number,
    }): Array<PageNum> {
        let pageLeftmost = args.pageCurrent - args.range
        let rangeContinuum = args.range * 2 + 1
        let pageArray: Array<PageNum> = []
        for (let increment = 0; increment < rangeContinuum; increment++) {
            let page = pageLeftmost + increment

            let isNotStartPage = page !== args.pageStart
            let isNotEndPage = page !== args.pageEnd
            let isInBoundary = (page >= args.pageStart) &&
                (page <= args.pageEnd)
            let isShouldBeIncluded = isNotStartPage && isNotEndPage && isInBoundary
            if (isShouldBeIncluded) {
                pageArray.push(page)
            }
        }
        return pageArray
    }

    /**
     * @example
     *     isLeftEllipsisRequired({pageStart: 1, pageCurrent: 6, range: 3}) === true
     *     isLeftEllipsisRequired({pageStart: 1, pageCurrent: 5, range: 3}) === false
     */
    isLeftEllipsisRequired(args: {
        pageStart: PageNum, pageCurrent: PageNum, range: number,
    }): boolean {
        let rangeLengthIncludingCurrentPageButton = args.range + 1
        let rangeEnd = args.pageCurrent - rangeLengthIncludingCurrentPageButton
        let isSpaceBetweenRangeEndAndPageEnd = rangeEnd > args.pageStart
        return isSpaceBetweenRangeEndAndPageEnd
    }
    
    /**
     * @example
     *     isRightEllipsisRequired({pageStart: 9, pageCurrent: 5, range: 3}) === false
     *     isRightEllipsisRequired({pageStart: 9, pageCurrent: 4, range: 3}) === true
     */
    isRightEllipsisRequired(args: {
        pageEnd: PageNum, pageCurrent: PageNum, range: number,
    }): boolean {
        let rangeLengthIncludingCurrentPageButton = args.range + 1
        let rangeEnd = args.pageCurrent + rangeLengthIncludingCurrentPageButton
        let isSpaceBetweenRangeEndAndPageEnd = rangeEnd < args.pageEnd
        return isSpaceBetweenRangeEndAndPageEnd
    }
}
