"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const http_1 = require("@angular/http");
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const core_1 = require("@angular/core");
let QueryDataToURLSearchParamsSerializer = class QueryDataToURLSearchParamsSerializer {
    toSearchParams(queryData) {
        this.params = new http_1.URLSearchParams();
        this.addAttrimClassesToParams(queryData);
        this.addPriceRangeToParams(queryData);
        this.addCategoryToParams(queryData);
        this.addSortingToParams(queryData);
        this.addPageToParams(queryData);
        return this.params;
    }
    addAttrimClassesToParams(queryData) {
        for (let cls of queryData.attrimClsArray) {
            let optionsSelected = cls.options.filter(option => option.isSelected === true);
            if (optionsSelected.length === 0) {
                continue;
            }
            let optionValuesList = optionsSelected.map(option => option.value);
            let optionValues = optionValuesList.join(',');
            this.params.set(`filter[attrim.${cls.code}]`, optionValues);
        }
    }
    addPriceRangeToParams(queryData) {
        let range = queryData.priceRange;
        this.params.set(`filter[price]`, `${range.min},${range.max}`);
    }
    addCategoryToParams(queryData) {
        if (queryData.categorySlug) {
            this.params.set('filter[category]', queryData.categorySlug);
        }
    }
    addSortingToParams(queryData) {
        switch (queryData.sorting) {
            case query_data_model_1.Sorting.NameAZ:
                this.params.set('sort', 'name');
                break;
            case query_data_model_1.Sorting.NameZA:
                this.params.set('sort', '-name');
                break;
            case query_data_model_1.Sorting.PriceMinMax:
                this.params.set('sort', 'price');
                break;
            case query_data_model_1.Sorting.PriceMaxMin:
                this.params.set('sort', '-price');
                break;
        }
    }
    addPageToParams(queryData) {
        this.params.set(`page`, String(queryData.pageCurrent));
    }
};
QueryDataToURLSearchParamsSerializer = __decorate([
    core_1.Injectable()
], QueryDataToURLSearchParamsSerializer);
exports.QueryDataToURLSearchParamsSerializer = QueryDataToURLSearchParamsSerializer;
//# sourceMappingURL=search-params.js.map