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
const page_range_service_1 = require("app/product-list/pagination-form/page-range.service");
let PageRangeComponent = class PageRangeComponent {
    constructor(pageRangeService) {
        this.pageRangeService = pageRangeService;
        this.updatedEvent = new core_4.EventEmitter();
        this.buttonRange = 3;
    }
    setPage(pageRaw) {
        this.queryData.pageCurrent = Number(pageRaw);
        this.updatedEvent.emit();
    }
    getPageArrayRange() {
        return this.pageRangeService.getPageArrayRange({
            pageStart: this.queryData.pageFirst,
            pageEnd: this.queryData.pageLast,
            pageCurrent: this.queryData.pageCurrent,
            range: this.buttonRange,
        });
    }
    isCurrentPage(pageRaw) {
        let page = Number(pageRaw);
        return this.queryData.pageCurrent === page;
    }
    isLeftEllipsisRequired() {
        return this.pageRangeService.isLeftEllipsisRequired({
            pageStart: this.queryData.pageFirst,
            pageCurrent: this.queryData.pageCurrent,
            range: this.buttonRange,
        });
    }
    isRightEllipsisRequired() {
        return this.pageRangeService.isRightEllipsisRequired({
            pageEnd: this.queryData.pageLast,
            pageCurrent: this.queryData.pageCurrent,
            range: this.buttonRange,
        });
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], PageRangeComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], PageRangeComponent.prototype, "updatedEvent", void 0);
PageRangeComponent = __decorate([
    core_1.Component({
        selector: 'page-range',
        moduleId: module.id,
        templateUrl: 'page-range.comp.html',
    }),
    __metadata("design:paramtypes", [page_range_service_1.PageRangeService])
], PageRangeComponent);
exports.PageRangeComponent = PageRangeComponent;
//# sourceMappingURL=page-range.comp.js.map