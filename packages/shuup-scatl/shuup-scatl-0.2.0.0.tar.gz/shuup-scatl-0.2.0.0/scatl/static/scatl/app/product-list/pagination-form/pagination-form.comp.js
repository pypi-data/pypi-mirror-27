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
const core_5 = require("@angular/core");
let PaginationFormComponent = class PaginationFormComponent {
    constructor() {
        this.updatedEvent = new core_4.EventEmitter();
    }
    updateQueryData() {
        this.updatedEvent.emit();
    }
    setPage(pageRaw) {
        this.queryData.pageCurrent = Number(pageRaw);
        this.updatedEvent.emit();
    }
    isCurrentPage(pageRaw) {
        let page = Number(pageRaw);
        return this.queryData.pageCurrent === page;
    }
    isEndButtonShouldBePresent() {
        return this.queryData.pageFirst !== this.queryData.pageLast;
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], PaginationFormComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], PaginationFormComponent.prototype, "updatedEvent", void 0);
PaginationFormComponent = __decorate([
    core_1.Component({
        selector: 'pagination-form',
        moduleId: module.id,
        templateUrl: 'pagination-form.comp.html',
        styleUrls: ['pagination-form.comp.css'],
        encapsulation: core_5.ViewEncapsulation.None,
    })
], PaginationFormComponent);
exports.PaginationFormComponent = PaginationFormComponent;
//# sourceMappingURL=pagination-form.comp.js.map