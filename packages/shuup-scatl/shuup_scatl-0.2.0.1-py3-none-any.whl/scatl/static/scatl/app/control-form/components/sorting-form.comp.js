"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
const core_2 = require("@angular/core");
const core_3 = require("@angular/core");
const core_4 = require("@angular/core");
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const query_data_model_2 = require("app/shared/query-data/query-data.model");
let SortingFormComponent = class SortingFormComponent {
    constructor() {
        this.sorting = query_data_model_2.Sorting;
        this.updatedEvent = new core_4.EventEmitter();
    }
    // noinspection JSUnusedGlobalSymbols
    setSorting(input) {
        let sortingSelectedKey = query_data_model_2.Sorting[input.value];
        let sortingSelected = query_data_model_2.Sorting[sortingSelectedKey];
        this.queryData.sorting = sortingSelected;
        this.updatedEvent.emit();
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], SortingFormComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], SortingFormComponent.prototype, "updatedEvent", void 0);
SortingFormComponent = __decorate([
    core_1.Component({
        selector: 'sorting-form',
        moduleId: module.id,
        templateUrl: 'sorting-form.comp.html',
        styleUrls: ['sorting-form.comp.css'],
    })
], SortingFormComponent);
exports.SortingFormComponent = SortingFormComponent;
//# sourceMappingURL=sorting-form.comp.js.map