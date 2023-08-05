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
const core_1 = require("@angular/core");
let JsonToQueryDataDeserializer = class JsonToQueryDataDeserializer {
    toQueryData(args) {
        // TODO what about the other initial data? it does not require deserialization?
        let queryData = args.dataInitial;
        queryData.attrimClsArray = this.deserializeAttrimClsArray(args.dataJson);
        queryData.pageLast = args.dataJson.page_last;
        return queryData;
    }
    deserializeAttrimClsArray(json) {
        let clsArray = [];
        let clsJsonArray = json.attrim_cls_list;
        for (let clsJson of clsJsonArray) {
            let options = [];
            for (let optionJson of clsJson.options) {
                let option = new query_data_model_2.AttrimOption({
                    value: optionJson.value,
                    isSelected: optionJson.is_selected,
                });
                options.push(option);
            }
            let cls = new query_data_model_1.AttrimCls({
                code: clsJson.code,
                name: clsJson.name,
                options: options,
            });
            clsArray.push(cls);
        }
        return clsArray;
    }
};
JsonToQueryDataDeserializer = __decorate([
    core_1.Injectable()
], JsonToQueryDataDeserializer);
exports.JsonToQueryDataDeserializer = JsonToQueryDataDeserializer;
//# sourceMappingURL=json.js.map