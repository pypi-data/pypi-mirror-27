"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const core_1 = require("@angular/core");
let QueryDataToRouteParamsSerializer = class QueryDataToRouteParamsSerializer {
    toRouteParams(queryData) {
        this.params = {};
        this.addAttrimClassesToParams(queryData);
        this.addPriceRangeToParams(queryData);
        this.addSortingToParams(queryData);
        this.addPagination(queryData);
        return this.params;
    }
    addAttrimClassesToParams(queryData) {
        for (let cls of queryData.attrimClsArray) {
            let optionsSelected = cls.options.filter(option => option.isSelected === true);
            if (optionsSelected.length === 0) {
                continue;
            }
            let optionValuesList = optionsSelected.map(option => option.value);
            let optionValues = optionValuesList.join('~');
            this.params[`filter.attrim.${cls.code}`] = optionValues;
        }
    }
    addPriceRangeToParams(queryData) {
        let range = queryData.priceRange;
        this.params[`filter.price`] = `${range.min}~${range.max}`;
    }
    addSortingToParams(queryData) {
        switch (queryData.sorting) {
            case query_data_model_1.Sorting.NameAZ:
                this.params['sort'] = 'name';
                break;
            case query_data_model_1.Sorting.NameZA:
                this.params['sort'] = '-name';
                break;
            case query_data_model_1.Sorting.PriceMinMax:
                this.params['sort'] = 'price';
                break;
            case query_data_model_1.Sorting.PriceMaxMin:
                this.params['sort'] = '-price';
                break;
        }
    }
    addPagination(queryData) {
        this.params['page'] = queryData.pageCurrent;
    }
};
QueryDataToRouteParamsSerializer = __decorate([
    core_1.Injectable()
], QueryDataToRouteParamsSerializer);
exports.QueryDataToRouteParamsSerializer = QueryDataToRouteParamsSerializer;
//# sourceMappingURL=route-params.js.map