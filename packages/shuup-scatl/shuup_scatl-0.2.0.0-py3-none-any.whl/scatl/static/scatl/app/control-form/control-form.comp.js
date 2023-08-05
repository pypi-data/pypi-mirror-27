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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
const query_data_service_1 = require("app/shared/query-data/query-data.service");
const product_list_service_1 = require("app/shared/product-list/product-list.service");
const router_1 = require("@angular/router");
const async_with_loading_bar_decorator_1 = require("app/shared/decorators/async-with-loading-bar.decorator");
const ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
const notify_service_1 = require("app/shared/notify.service");
const with_notify_decorator_1 = require("app/shared/decorators/with-notify.decorator");
let ControlFormComponent = class ControlFormComponent {
    // noinspection JSUnusedGlobalSymbols
    constructor(loadingBarService, notifyService, queryDataService, activatedRoute, productListService) {
        this.loadingBarService = loadingBarService;
        this.notifyService = notifyService;
        this.queryDataService = queryDataService;
        this.activatedRoute = activatedRoute;
        this.productListService = productListService;
    }
    ngOnInit() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.loadQueryDataFromUrl();
            yield this.handleQueryDataUpdate();
        });
    }
    handleQueryDataUpdate() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.queryDataService.updateQueryData();
            yield this.productListService.updateList();
        });
    }
    loadQueryDataFromUrl() {
        this.queryDataService.initQueryDataFromPageUrl(this.activatedRoute.snapshot);
    }
};
__decorate([
    async_with_loading_bar_decorator_1.asyncWithLoadingBar,
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ControlFormComponent.prototype, "handleQueryDataUpdate", null);
__decorate([
    with_notify_decorator_1.withNotify({ onErrorMsg: {
            header: `URL error`,
            body: `Can't read the filters from the url, is the provided url correct?`,
        } }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], ControlFormComponent.prototype, "loadQueryDataFromUrl", null);
ControlFormComponent = __decorate([
    core_1.Component({
        selector: 'control-form',
        moduleId: module.id,
        templateUrl: 'control-form.comp.html',
        styleUrls: ['control-form.comp.css'],
    }),
    __metadata("design:paramtypes", [ng2_slim_loading_bar_1.SlimLoadingBarService,
        notify_service_1.NotifyService,
        query_data_service_1.QueryDataService,
        router_1.ActivatedRoute,
        product_list_service_1.ProductListService])
], ControlFormComponent);
exports.ControlFormComponent = ControlFormComponent;
//# sourceMappingURL=control-form.comp.js.map