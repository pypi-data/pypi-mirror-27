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
const http_1 = require("@angular/http");
const json_1 = require("app/shared/product-list/deserializers/json");
const search_params_1 = require("app/shared/query-data/serializers/search-params");
const query_data_service_1 = require("app/shared/query-data/query-data.service");
const with_notify_decorator_1 = require("app/shared/decorators/with-notify.decorator");
const notify_service_1 = require("app/shared/notify.service");
let ProductListService = class ProductListService {
    // noinspection JSUnusedGlobalSymbols
    constructor(notifyService, http, paramsSerializer, queryDataService) {
        this.notifyService = notifyService;
        this.http = http;
        this.paramsSerializer = paramsSerializer;
        this.queryDataService = queryDataService;
        this.productListUrl = `/api/scatl/front/products/`;
    }
    updateList() {
        return __awaiter(this, void 0, void 0, function* () {
            this.rejectPromise(this.productListPromise);
            this.productList = yield this.getProductList();
        });
    }
    getProductList() {
        return __awaiter(this, void 0, void 0, function* () {
            let params = this.paramsSerializer.toSearchParams(this.queryDataService.queryData);
            let productListObservable = this.http
                .get(this.productListUrl, { search: params })
                .map(json_1.deserializeProductList);
            this.productListPromise = productListObservable.toPromise();
            return this.productListPromise;
        });
    }
    rejectPromise(promise) {
        if (promise === undefined) {
            return;
        }
        let returnOldProductList = () => this.productList;
        promise.then(returnOldProductList);
    }
};
__decorate([
    with_notify_decorator_1.asyncWithNotify({ onErrorMsg: { header: `Product list update error` } }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ProductListService.prototype, "getProductList", null);
ProductListService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [notify_service_1.NotifyService,
        http_1.Http,
        search_params_1.QueryDataToURLSearchParamsSerializer,
        query_data_service_1.QueryDataService])
], ProductListService);
exports.ProductListService = ProductListService;
//# sourceMappingURL=product-list.service.js.map