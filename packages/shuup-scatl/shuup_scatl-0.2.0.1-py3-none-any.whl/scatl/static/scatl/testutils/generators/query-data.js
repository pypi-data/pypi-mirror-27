"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const query_data_model_2 = require("app/shared/query-data/query-data.model");
const query_data_model_3 = require("app/shared/query-data/query-data.model");
const query_data_model_4 = require("app/shared/query-data/query-data.model");
const unique_1 = require("testutils/generators/unique");
const enums_1 = require("testutils/enums");
const query_data_model_5 = require("app/shared/query-data/query-data.model");
class QueryDataGenerator {
    constructor() {
        this.fake = faker;
        this.uniqueGen = new unique_1.UniqueGenerator();
    }
    data() {
        let data = new query_data_model_1.QueryData({
            attrimClsArray: this.attrimClsArray(),
            priceRange: this.priceRange(),
            sorting: this.sorting(),
            pageCurrent: this.fake.random.number({ min: 1, max: 50 }),
            pageLast: this.fake.random.number({ min: 50, max: 100 }),
        });
        return data;
    }
    sorting() {
        let sortingRandom = enums_1.getSampleFromEnum(query_data_model_2.Sorting);
        return sortingRandom;
    }
    attrimClsArray(amount = 5) {
        let classes = [];
        for (let num = 0; num <= amount; num++) {
            classes.push(this.attrimCls());
        }
        return classes;
    }
    attrimCls(optionsAmount = 5) {
        let code = this.uniqueGen.word();
        let cls = new query_data_model_3.AttrimCls({
            code: code,
            name: code,
            options: this.attrimOptionArray(optionsAmount),
        });
        return cls;
    }
    attrimOptionArray(amount = 5) {
        let options = [];
        let uniqueGen = new unique_1.UniqueGenerator();
        for (let num = 0; num <= amount; num++) {
            let option = this.attrimOption({ value: uniqueGen.word() });
            options.push(option);
        }
        return options;
    }
    attrimOption(args) {
        let option = new query_data_model_4.AttrimOption({
            value: args.value,
            isSelected: this.fake.random.boolean(),
        });
        return option;
    }
    priceRange() {
        let min, max;
        if (window.DJANGO === undefined) {
            min = this.fake.random.number();
            max = this.fake.random.number({ min: min });
        }
        else {
            min = window.DJANGO.priceRange.min;
            max = window.DJANGO.priceRange.max;
        }
        let range = new query_data_model_5.PriceRange(min, max);
        return range;
    }
}
exports.QueryDataGenerator = QueryDataGenerator;
//# sourceMappingURL=query-data.js.map