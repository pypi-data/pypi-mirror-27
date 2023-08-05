"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const query_data_model_2 = require("app/shared/query-data/query-data.model");
const query_data_model_3 = require("app/shared/query-data/query-data.model");
const query_data_model_4 = require("app/shared/query-data/query-data.model");
const app_routing_1 = require("app/app.routing");
const query_data_model_5 = require("app/shared/query-data/query-data.model");
const core_1 = require("@angular/core");
let RouteSnapshotToQueryDataDeserializer = class RouteSnapshotToQueryDataDeserializer {
    toQueryData(routeSnapshot) {
        this.routeSnapshot = routeSnapshot;
        let queryData = new query_data_model_4.QueryData({
            attrimClsArray: this.deserializeAttrimClsArray(),
            priceRange: this.deserializePriceRange(),
            categorySlug: this.deserializeCategorySlug(),
            sorting: this.deserializeSorting(),
            pageCurrent: this.deserializePageCurrent(),
            pageLast: this.deserializePageLast(),
        });
        return queryData;
    }
    deserializeCategorySlug() {
        let routeLocationCurrent = this.routeSnapshot.data[`location`];
        let isUrlContainsCategory = routeLocationCurrent === app_routing_1.routeLocation.category;
        if (isUrlContainsCategory) {
            let currentUrl = this.getCurrentUrl(this.routeSnapshot);
            let categorySlugMatch = /([\w\-]+)?\/?$/g.exec(currentUrl);
            let isCategorySlugNotFound = categorySlugMatch === null;
            if (isCategorySlugNotFound) {
                return null;
            }
            let categorySlug = categorySlugMatch[1];
            return categorySlug;
        }
        else {
            return null;
        }
    }
    deserializeAttrimClsArray() {
        let clsArray = [];
        let regexForClsCode = /filter\.attrim\.(\w+)/i;
        for (let paramName in this.routeSnapshot.params) {
            let clsCodeMatch = paramName.match(regexForClsCode);
            if (!clsCodeMatch) {
                // it's ok, the params can contain not only attrim classes
                continue;
            }
            let clsCode = clsCodeMatch[1];
            let cls = new query_data_model_2.AttrimCls({ code: clsCode });
            // TODO assert valid string
            let optionValues = this.routeSnapshot.params[paramName].split(`~`);
            for (let optionValue of optionValues) {
                let option = new query_data_model_3.AttrimOption({
                    value: optionValue,
                    isSelected: true,
                });
                cls.options.push(option);
            }
            clsArray.push(cls);
        }
        return clsArray;
    }
    deserializePriceRange() {
        let params = this.routeSnapshot.params;
        for (let paramName in params) {
            let isPriceRangeParam = paramName.indexOf(`filter.price`) !== -1;
            if (isPriceRangeParam) {
                let rangeValuesStr = params[paramName];
                this.validateRangeValues(rangeValuesStr);
                let rangeValuesRaw = params[paramName].split(`~`);
                let min = Number(rangeValuesRaw[0]);
                let max = Number(rangeValuesRaw[1]);
                return new query_data_model_5.PriceRange(min, max);
            }
        }
        return new query_data_model_5.PriceRange(window.DJANGO.priceRange.min, window.DJANGO.priceRange.max);
    }
    deserializeSorting() {
        let sortingParamKey = `sort`;
        let sortType = this.routeSnapshot.params[sortingParamKey];
        switch (sortType) {
            case `name`:
                return query_data_model_1.Sorting.NameAZ;
            case `-name`:
                return query_data_model_1.Sorting.NameZA;
            case `price`:
                return query_data_model_1.Sorting.PriceMinMax;
            case `-price`:
                return query_data_model_1.Sorting.PriceMaxMin;
            default:
                return query_data_model_1.Sorting.NameAZ;
        }
    }
    deserializePageCurrent() {
        let page;
        if (`page` in this.routeSnapshot.params) {
            page = Number(this.routeSnapshot.params[`page`]);
        }
        else {
            page = 1;
        }
        return page;
    }
    deserializePageLast() {
        let pageLast;
        if (`last` in this.routeSnapshot.params) {
            pageLast = Number(this.routeSnapshot.params[`last`]);
        }
        else {
            pageLast = 1;
        }
        return pageLast;
    }
    getCurrentUrl(snapshot) {
        let urlPaths = [];
        for (let urlSegment of snapshot.url) {
            urlPaths.push(urlSegment.path);
        }
        let currentUrl = urlPaths.join(`/`);
        return currentUrl;
    }
    validateRangeValues(priceRangeValuesRaw) {
        let errorMessage = 'Invalid price range parameter';
        let rangeMatch = /^[0-9]+~[0-9]+$/g.exec(priceRangeValuesRaw);
        if (rangeMatch === null) {
            throw Error(errorMessage);
        }
    }
};
RouteSnapshotToQueryDataDeserializer = __decorate([
    core_1.Injectable()
], RouteSnapshotToQueryDataDeserializer);
exports.RouteSnapshotToQueryDataDeserializer = RouteSnapshotToQueryDataDeserializer;
//# sourceMappingURL=route-snapshot.js.map