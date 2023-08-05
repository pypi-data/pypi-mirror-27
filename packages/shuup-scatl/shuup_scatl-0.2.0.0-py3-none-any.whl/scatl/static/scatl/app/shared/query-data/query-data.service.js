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
const router_1 = require("@angular/router");
const route_snapshot_1 = require("app/shared/query-data/deserializers/route-snapshot");
const route_params_1 = require("app/shared/query-data/serializers/route-params");
const query_data_network_service_1 = require("app/shared/query-data/query-data-network.service");
const with_notify_decorator_1 = require("app/shared/decorators/with-notify.decorator");
const notify_service_1 = require("app/shared/notify.service");
let QueryDataService = class QueryDataService {
    // noinspection JSUnusedGlobalSymbols
    constructor(notifyService, router, queryDataNetworkService, routeSnapshotDeserializer, routeParamsSerializer) {
        this.notifyService = notifyService;
        this.router = router;
        this.queryDataNetworkService = queryDataNetworkService;
        this.routeSnapshotDeserializer = routeSnapshotDeserializer;
        this.routeParamsSerializer = routeParamsSerializer;
    }
    /**
     * It must receive ActivatedRouteSnapshot externally because otherwise
     * angular will inject in service only the default root routers, while
     * here it needs the current one.
     */
    initQueryDataFromPageUrl(routeSnapshot) {
        this.queryData = this.routeSnapshotDeserializer.toQueryData(routeSnapshot);
    }
    updateQueryData() {
        return __awaiter(this, void 0, void 0, function* () {
            this.updatePageUrlAccordingToQueryData();
            yield this.updateQueryDataFromServer();
        });
    }
    updatePageUrlAccordingToQueryData() {
        let queryDataParamsNew = this.routeParamsSerializer.toRouteParams(this.queryData);
        let currentRouterLocation = `.`;
        // noinspection JSIgnoredPromiseFromCall
        this.router.navigate([currentRouterLocation, queryDataParamsNew]);
    }
    updateQueryDataFromServer() {
        this.rejectPromise(this.queryDataPromise);
        this.queryDataPromise = this.queryDataNetworkService.update(this.queryData);
        this.queryDataPromise.then(qs => this.queryData = qs);
        return this.queryDataPromise;
    }
    rejectPromise(promise) {
        if (promise === undefined) {
            return;
        }
        let returnOldQueryData = () => this.queryData;
        promise.then(returnOldQueryData);
    }
};
__decorate([
    with_notify_decorator_1.asyncWithNotify({ onErrorMsg: { header: `Filters update error` } }),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], QueryDataService.prototype, "updateQueryData", null);
QueryDataService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [notify_service_1.NotifyService,
        router_1.Router,
        query_data_network_service_1.QueryDataNetworkService,
        route_snapshot_1.RouteSnapshotToQueryDataDeserializer,
        route_params_1.QueryDataToRouteParamsSerializer])
], QueryDataService);
exports.QueryDataService = QueryDataService;
//# sourceMappingURL=query-data.service.js.map