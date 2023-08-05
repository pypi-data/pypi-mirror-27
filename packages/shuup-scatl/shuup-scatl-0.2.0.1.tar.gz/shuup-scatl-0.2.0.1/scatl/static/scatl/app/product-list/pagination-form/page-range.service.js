"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
let PageRangeService = class PageRangeService {
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
    getPageArrayRange(args) {
        let pageLeftmost = args.pageCurrent - args.range;
        let rangeContinuum = args.range * 2 + 1;
        let pageArray = [];
        for (let increment = 0; increment < rangeContinuum; increment++) {
            let page = pageLeftmost + increment;
            let isNotStartPage = page !== args.pageStart;
            let isNotEndPage = page !== args.pageEnd;
            let isInBoundary = (page >= args.pageStart) &&
                (page <= args.pageEnd);
            let isShouldBeIncluded = isNotStartPage && isNotEndPage && isInBoundary;
            if (isShouldBeIncluded) {
                pageArray.push(page);
            }
        }
        return pageArray;
    }
    /**
     * @example
     *     isLeftEllipsisRequired({pageStart: 1, pageCurrent: 6, range: 3}) === true
     *     isLeftEllipsisRequired({pageStart: 1, pageCurrent: 5, range: 3}) === false
     */
    isLeftEllipsisRequired(args) {
        let rangeLengthIncludingCurrentPageButton = args.range + 1;
        let rangeEnd = args.pageCurrent - rangeLengthIncludingCurrentPageButton;
        let isSpaceBetweenRangeEndAndPageEnd = rangeEnd > args.pageStart;
        return isSpaceBetweenRangeEndAndPageEnd;
    }
    /**
     * @example
     *     isRightEllipsisRequired({pageStart: 9, pageCurrent: 5, range: 3}) === false
     *     isRightEllipsisRequired({pageStart: 9, pageCurrent: 4, range: 3}) === true
     */
    isRightEllipsisRequired(args) {
        let rangeLengthIncludingCurrentPageButton = args.range + 1;
        let rangeEnd = args.pageCurrent + rangeLengthIncludingCurrentPageButton;
        let isSpaceBetweenRangeEndAndPageEnd = rangeEnd < args.pageEnd;
        return isSpaceBetweenRangeEndAndPageEnd;
    }
};
PageRangeService = __decorate([
    core_1.Injectable()
], PageRangeService);
exports.PageRangeService = PageRangeService;
//# sourceMappingURL=page-range.service.js.map