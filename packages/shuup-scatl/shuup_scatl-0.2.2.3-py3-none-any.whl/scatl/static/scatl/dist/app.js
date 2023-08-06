webpackJsonp([1],{

/***/ 102:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const router_1 = __webpack_require__(93);
const route_snapshot_1 = __webpack_require__(308);
const route_params_1 = __webpack_require__(309);
const query_data_network_service_1 = __webpack_require__(310);
const with_notify_decorator_1 = __webpack_require__(155);
const notify_service_1 = __webpack_require__(103);
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


/***/ }),

/***/ 103:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const angular2_notifications_1 = __webpack_require__(151);
let NotifyService = class NotifyService {
    constructor(service) {
        this.service = service;
        this.config = {
            timeOut: 5000,
            showProgressBar: true,
            pauseOnHover: true,
            clickToClose: true,
        };
    }
    error(title, content = '') {
        this.service.error(title, content, this.config);
    }
    success(title, content = '') {
        this.service.success(title, content, this.config);
    }
};
NotifyService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [angular2_notifications_1.NotificationsService])
], NotifyService);
exports.NotifyService = NotifyService;


/***/ }),

/***/ 153:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const http_1 = __webpack_require__(70);
const json_1 = __webpack_require__(763);
const search_params_1 = __webpack_require__(154);
const query_data_service_1 = __webpack_require__(102);
const with_notify_decorator_1 = __webpack_require__(155);
const notify_service_1 = __webpack_require__(103);
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


/***/ }),

/***/ 154:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const http_1 = __webpack_require__(70);
const query_data_model_1 = __webpack_require__(20);
const core_1 = __webpack_require__(3);
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


/***/ }),

/***/ 155:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
function withNotify(messages) {
    return (target, propertyKey, descriptor) => {
        let originalMethod = descriptor.value;
        descriptor.value = function (...args) {
            let notifyService = this.notifyService;
            let result;
            try {
                result = originalMethod.apply(this, args);
                showSuccessNotify(notifyService, messages);
            }
            catch (error) {
                showErrorNotify(notifyService, messages, error);
            }
            return result;
        };
        return descriptor;
    };
}
exports.withNotify = withNotify;
/** It will break without the semicolons. */
function asyncWithNotify(messages) {
    return (target, propertyKey, descriptor) => {
        let originalMethod = descriptor.value;
        descriptor.value = function (...args) {
            return __awaiter(this, void 0, void 0, function* () {
                let notifyService = this.notifyService;
                let result;
                try {
                    result = yield originalMethod.apply(this, args);
                    showSuccessNotify(notifyService, messages);
                }
                catch (error) {
                    showErrorNotify(notifyService, messages, error);
                }
                return result;
            });
        };
        return descriptor;
    };
}
exports.asyncWithNotify = asyncWithNotify;
function showSuccessNotify(notifyService, messages) {
    if (messages.onSuccessMsg !== undefined) {
        notifyService.success(messages.onSuccessMsg);
    }
}
function showErrorNotify(notifyService, messages, error) {
    let errorMsgBody;
    if (messages.onErrorMsg.body === undefined) {
        errorMsgBody = `${error}`;
    }
    else {
        errorMsgBody = `${messages.onErrorMsg.body}<br>${error}`;
    }
    notifyService.error(messages.onErrorMsg.header, errorMsgBody);
}


/***/ }),

/***/ 20:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
class QueryData {
    constructor(args) {
        this.sorting = Sorting.PriceMinMax;
        this.categorySlug = null;
        this.pageCurrent = 1;
        this.pageFirst = 1;
        this.pageLast = 1;
        this.attrimClsArray = args.attrimClsArray;
        this.priceRange = args.priceRange;
        this.sorting = args.sorting ? args.sorting : this.sorting;
        this.categorySlug = args.categorySlug ? args.categorySlug : this.categorySlug;
        this.pageCurrent = args.pageCurrent ? args.pageCurrent : this.pageCurrent;
        this.pageLast = args.pageLast ? args.pageLast : this.pageLast;
    }
}
exports.QueryData = QueryData;
var Sorting;
(function (Sorting) {
    Sorting[Sorting["NameAZ"] = 0] = "NameAZ";
    Sorting[Sorting["NameZA"] = 1] = "NameZA";
    Sorting[Sorting["PriceMinMax"] = 2] = "PriceMinMax";
    Sorting[Sorting["PriceMaxMin"] = 3] = "PriceMaxMin";
})(Sorting = exports.Sorting || (exports.Sorting = {}));
class AttrimCls {
    constructor(args) {
        this.code = args.code;
        this.options = args.options || [];
        this.name = args.name || this.code;
    }
}
exports.AttrimCls = AttrimCls;
class AttrimOption {
    constructor(args) {
        this.isSelected = false;
        this.value = args.value;
        this.isSelected = args.isSelected || this.isSelected;
    }
}
exports.AttrimOption = AttrimOption;
var ShuupAttrType;
(function (ShuupAttrType) {
    ShuupAttrType[ShuupAttrType["BOOLEAN"] = 2] = "BOOLEAN";
})(ShuupAttrType = exports.ShuupAttrType || (exports.ShuupAttrType = {}));
class ShuupAttr {
    constructor(args) {
        this.identifier = args.identifier;
        this.type = args.type;
        this.value = args.value;
    }
}
exports.ShuupAttr = ShuupAttr;
class PriceRange {
    constructor(min, max) {
        this.min = min;
        this.max = max;
    }
}
exports.PriceRange = PriceRange;


/***/ }),

/***/ 306:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
const router_1 = __webpack_require__(93);
const catalog_comp_1 = __webpack_require__(307);
exports.routeLocation = {
    root: 'root',
    category: 'category',
};
const routes = [
    {
        // TODO allow to defined it with the plugin or admin config
        path: 'catalog',
        component: catalog_comp_1.CatalogComponent,
        data: {
            location: exports.routeLocation.root,
        },
    },
    // TODO: don't forget about 404 here
    {
        path: '**',
        component: catalog_comp_1.CatalogComponent,
        data: {
            location: exports.routeLocation.category,
        },
    },
];
exports.routing = router_1.RouterModule.forRoot(routes);


/***/ }),

/***/ 307:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(3);
const core_2 = __webpack_require__(3);
let CatalogComponent = class CatalogComponent {
};
CatalogComponent = __decorate([
    core_1.Component({
        selector: 'catalog',
        template: __webpack_require__(759),
        styles: [__webpack_require__(760)],
        encapsulation: core_2.ViewEncapsulation.None,
    })
], CatalogComponent);
exports.CatalogComponent = CatalogComponent;


/***/ }),

/***/ 308:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const query_data_model_1 = __webpack_require__(20);
const query_data_model_2 = __webpack_require__(20);
const query_data_model_3 = __webpack_require__(20);
const query_data_model_4 = __webpack_require__(20);
const app_routing_1 = __webpack_require__(306);
const query_data_model_5 = __webpack_require__(20);
const core_1 = __webpack_require__(3);
let RouteSnapshotToQueryDataDeserializer = class RouteSnapshotToQueryDataDeserializer {
    toQueryData(routeSnapshot) {
        this.routeSnapshot = routeSnapshot;
        let queryData = new query_data_model_4.QueryData({
            attrimClsArray: this.deserializeAttrimClsArray(),
            priceRange: this.deserializePriceRange(),
            categorySlug: this.deserializeCategorySlug(),
            sorting: this.deserializeSorting(),
            pageCurrent: this.deserializePageCurrent(),
            pageLast: this.deserializePageLast(),
        });
        return queryData;
    }
    deserializeCategorySlug() {
        let routeLocationCurrent = this.routeSnapshot.data[`location`];
        let isUrlContainsCategory = routeLocationCurrent === app_routing_1.routeLocation.category;
        if (isUrlContainsCategory) {
            let currentUrl = this.getCurrentUrl(this.routeSnapshot);
            let categorySlugMatch = /([\w\-]+)?\/?$/g.exec(currentUrl);
            let isCategorySlugNotFound = categorySlugMatch === null;
            if (isCategorySlugNotFound) {
                return null;
            }
            let categorySlug = categorySlugMatch[1];
            return categorySlug;
        }
        else {
            return null;
        }
    }
    deserializeAttrimClsArray() {
        let clsArray = [];
        let regexForClsCode = /filter\.attrim\.(\w+)/i;
        for (let paramName in this.routeSnapshot.params) {
            let clsCodeMatch = paramName.match(regexForClsCode);
            if (!clsCodeMatch) {
                // it's ok, the params can contain not only attrim classes
                continue;
            }
            let clsCode = clsCodeMatch[1];
            let cls = new query_data_model_2.AttrimCls({ code: clsCode });
            // TODO assert valid string
            let optionValues = this.routeSnapshot.params[paramName].split(`~`);
            for (let optionValue of optionValues) {
                let option = new query_data_model_3.AttrimOption({
                    value: optionValue,
                    isSelected: true,
                });
                cls.options.push(option);
            }
            clsArray.push(cls);
        }
        return clsArray;
    }
    deserializePriceRange() {
        let params = this.routeSnapshot.params;
        for (let paramName in params) {
            let isPriceRangeParam = paramName.indexOf(`filter.price`) !== -1;
            if (isPriceRangeParam) {
                let rangeValuesStr = params[paramName];
                this.validateRangeValues(rangeValuesStr);
                let rangeValuesRaw = params[paramName].split(`~`);
                let min = Number(rangeValuesRaw[0]);
                let max = Number(rangeValuesRaw[1]);
                return new query_data_model_5.PriceRange(min, max);
            }
        }
        return new query_data_model_5.PriceRange(window.DJANGO.priceRange.min, window.DJANGO.priceRange.max);
    }
    deserializeSorting() {
        let sortingParamKey = `sort`;
        let sortType = this.routeSnapshot.params[sortingParamKey];
        switch (sortType) {
            case `price`:
                return query_data_model_1.Sorting.PriceMinMax;
            case `-price`:
                return query_data_model_1.Sorting.PriceMaxMin;
            case `name`:
                return query_data_model_1.Sorting.NameAZ;
            case `-name`:
                return query_data_model_1.Sorting.NameZA;
            default:
                return null;
        }
    }
    deserializePageCurrent() {
        let page;
        if (`page` in this.routeSnapshot.params) {
            page = Number(this.routeSnapshot.params[`page`]);
        }
        else {
            page = 1;
        }
        return page;
    }
    deserializePageLast() {
        let pageLast;
        if (`last` in this.routeSnapshot.params) {
            pageLast = Number(this.routeSnapshot.params[`last`]);
        }
        else {
            pageLast = 1;
        }
        return pageLast;
    }
    getCurrentUrl(snapshot) {
        let urlPaths = [];
        for (let urlSegment of snapshot.url) {
            urlPaths.push(urlSegment.path);
        }
        let currentUrl = urlPaths.join(`/`);
        return currentUrl;
    }
    validateRangeValues(priceRangeValuesRaw) {
        let errorMessage = 'Invalid price range parameter';
        let rangeMatch = /^[0-9]+~[0-9]+$/g.exec(priceRangeValuesRaw);
        if (rangeMatch === null) {
            throw Error(errorMessage);
        }
    }
};
RouteSnapshotToQueryDataDeserializer = __decorate([
    core_1.Injectable()
], RouteSnapshotToQueryDataDeserializer);
exports.RouteSnapshotToQueryDataDeserializer = RouteSnapshotToQueryDataDeserializer;


/***/ }),

/***/ 309:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const query_data_model_1 = __webpack_require__(20);
const core_1 = __webpack_require__(3);
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


/***/ }),

/***/ 310:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const http_1 = __webpack_require__(70);
const search_params_1 = __webpack_require__(154);
const json_1 = __webpack_require__(311);
let QueryDataNetworkService = class QueryDataNetworkService {
    constructor(http, queryDataSerializer, queryDataDeserializer) {
        this.http = http;
        this.queryDataSerializer = queryDataSerializer;
        this.queryDataDeserializer = queryDataDeserializer;
        this.url = `/api/scatl/front/query-data/`;
    }
    update(queryData) {
        return __awaiter(this, void 0, void 0, function* () {
            let params = this.queryDataSerializer.toSearchParams(queryData);
            let observable = this.http.get(this.url, { search: params })
                .retry(2)
                .map((response) => {
                return this.queryDataDeserializer.toQueryData({
                    dataJson: response.json(),
                    dataInitial: queryData,
                });
            });
            return observable.toPromise();
        });
    }
};
QueryDataNetworkService = __decorate([
    core_1.Injectable(),
    __metadata("design:paramtypes", [http_1.Http,
        search_params_1.QueryDataToURLSearchParamsSerializer,
        json_1.JsonToQueryDataDeserializer])
], QueryDataNetworkService);
exports.QueryDataNetworkService = QueryDataNetworkService;


/***/ }),

/***/ 311:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const query_data_model_1 = __webpack_require__(20);
const query_data_model_2 = __webpack_require__(20);
const core_1 = __webpack_require__(3);
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


/***/ }),

/***/ 312:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
function asyncWithLoadingBar(target, propertyKey, descriptor) {
    let originalMethod = descriptor.value;
    descriptor.value = function (...args) {
        return __awaiter(this, void 0, void 0, function* () {
            this.loadingBarService.start();
            let result = yield originalMethod.apply(this, args);
            this.loadingBarService.complete();
            return result;
        });
    };
    return descriptor;
}
exports.asyncWithLoadingBar = asyncWithLoadingBar;


/***/ }),

/***/ 313:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(3);
let PageRangeService = class PageRangeService {
    /**
     * @example
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 20, pageCurrent: 10, range: 3,
     *     }) === [7, 8, 9, 10, 11, 12, 13]
     *
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 20, pageCurrent: 10, range: 2,
     *     }) === [8, 9, 10, 11, 12]
     *
     *     // the start and the end pages aren't included
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 7, pageCurrent: 4, range: 3,
     *     }) === [2, 3, 4, 5, 6]
     *
     *     getPageArrayRange({
     *         pageStart: 1, pageEnd: 1, pageCurrent: 1, range: 3,
     *     }) === []
     */
    getPageArrayRange(args) {
        let pageLeftmost = args.pageCurrent - args.range;
        let rangeContinuum = args.range * 2 + 1;
        let pageArray = [];
        for (let increment = 0; increment < rangeContinuum; increment++) {
            let page = pageLeftmost + increment;
            let isNotStartPage = page !== args.pageStart;
            let isNotEndPage = page !== args.pageEnd;
            let isInBoundary = (page >= args.pageStart) &&
                (page <= args.pageEnd);
            let isShouldBeIncluded = isNotStartPage && isNotEndPage && isInBoundary;
            if (isShouldBeIncluded) {
                pageArray.push(page);
            }
        }
        return pageArray;
    }
    /**
     * @example
     *     isLeftEllipsisRequired({pageStart: 1, pageCurrent: 6, range: 3}) === true
     *     isLeftEllipsisRequired({pageStart: 1, pageCurrent: 5, range: 3}) === false
     */
    isLeftEllipsisRequired(args) {
        let rangeLengthIncludingCurrentPageButton = args.range + 1;
        let rangeEnd = args.pageCurrent - rangeLengthIncludingCurrentPageButton;
        let isSpaceBetweenRangeEndAndPageEnd = rangeEnd > args.pageStart;
        return isSpaceBetweenRangeEndAndPageEnd;
    }
    /**
     * @example
     *     isRightEllipsisRequired({pageStart: 9, pageCurrent: 5, range: 3}) === false
     *     isRightEllipsisRequired({pageStart: 9, pageCurrent: 4, range: 3}) === true
     */
    isRightEllipsisRequired(args) {
        let rangeLengthIncludingCurrentPageButton = args.range + 1;
        let rangeEnd = args.pageCurrent + rangeLengthIncludingCurrentPageButton;
        let isSpaceBetweenRangeEndAndPageEnd = rangeEnd < args.pageEnd;
        return isSpaceBetweenRangeEndAndPageEnd;
    }
};
PageRangeService = __decorate([
    core_1.Injectable()
], PageRangeService);
exports.PageRangeService = PageRangeService;


/***/ }),

/***/ 757:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
__webpack_require__(142);
const platform_browser_dynamic_1 = __webpack_require__(201);
const app_module_1 = __webpack_require__(758);
const core_1 = __webpack_require__(3);
core_1.enableProdMode();
platform_browser_dynamic_1.platformBrowserDynamic().bootstrapModule(app_module_1.AppModule);


/***/ }),

/***/ 758:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(3);
const forms_1 = __webpack_require__(60);
const forms_2 = __webpack_require__(60);
const forms_3 = __webpack_require__(60);
const platform_browser_1 = __webpack_require__(45);
const http_1 = __webpack_require__(70);
const animations_1 = __webpack_require__(200);
const ng2_nouislider_1 = __webpack_require__(303);
const angular2_notifications_1 = __webpack_require__(151);
const ng2_slim_loading_bar_1 = __webpack_require__(101);
const app_routing_1 = __webpack_require__(306);
const app_comp_1 = __webpack_require__(761);
const product_list_comp_1 = __webpack_require__(762);
const control_form_comp_1 = __webpack_require__(766);
const query_data_network_service_1 = __webpack_require__(310);
const product_list_service_1 = __webpack_require__(153);
const catalog_comp_1 = __webpack_require__(307);
const attrim_form_comp_1 = __webpack_require__(769);
const sorting_form_comp_1 = __webpack_require__(772);
const price_range_form_comp_1 = __webpack_require__(775);
const pagination_form_comp_1 = __webpack_require__(778);
const page_range_service_1 = __webpack_require__(313);
const route_params_1 = __webpack_require__(309);
const route_snapshot_1 = __webpack_require__(308);
const search_params_1 = __webpack_require__(154);
const json_1 = __webpack_require__(311);
const page_range_comp_1 = __webpack_require__(781);
const query_data_service_1 = __webpack_require__(102);
const notify_service_1 = __webpack_require__(103);
let AppModule = class AppModule {
};
AppModule = __decorate([
    core_1.NgModule({
        imports: [
            platform_browser_1.BrowserModule,
            animations_1.BrowserAnimationsModule,
            forms_1.FormsModule,
            http_1.HttpModule,
            forms_2.ReactiveFormsModule,
            app_routing_1.routing,
            ng2_nouislider_1.NouisliderModule,
            ng2_slim_loading_bar_1.SlimLoadingBarModule.forRoot(),
            angular2_notifications_1.SimpleNotificationsModule.forRoot(),
        ],
        declarations: [
            app_comp_1.AppComponent,
            catalog_comp_1.CatalogComponent,
            control_form_comp_1.ControlFormComponent,
            attrim_form_comp_1.AttrimFormComponent,
            sorting_form_comp_1.SortingFormComponent,
            price_range_form_comp_1.PriceRangeFormComponent,
            pagination_form_comp_1.PaginationFormComponent,
            page_range_comp_1.PageRangeComponent,
            product_list_comp_1.ProductListComponent,
        ],
        bootstrap: [app_comp_1.AppComponent],
        providers: [
            forms_3.FormBuilder,
            notify_service_1.NotifyService,
            product_list_service_1.ProductListService,
            page_range_service_1.PageRangeService,
            query_data_service_1.QueryDataService,
            query_data_network_service_1.QueryDataNetworkService,
            route_params_1.QueryDataToRouteParamsSerializer,
            search_params_1.QueryDataToURLSearchParamsSerializer,
            route_snapshot_1.RouteSnapshotToQueryDataDeserializer,
            json_1.JsonToQueryDataDeserializer,
        ],
    })
], AppModule);
exports.AppModule = AppModule;


/***/ }),

/***/ 759:
/***/ (function(module, exports) {

module.exports = "<ng2-slim-loading-bar [color]=\"&quot;#3fb8af&quot;\" [height]=\"&quot;2px&quot;\"></ng2-slim-loading-bar><simple-notifications></simple-notifications><div class=\"row\"><control-form class=\"col-md-3\"></control-form><product-list class=\"col-md-9\"></product-list></div>";

/***/ }),

/***/ 760:
/***/ (function(module, exports) {

module.exports = ".slim-loading-bar {\n  position: fixed;\n  margin: 0;\n  padding: 0;\n  top: 0;\n  left: 0;\n  right: 0;\n  z-index: 99999; }\n  .slim-loading-bar .slim-loading-bar-progress {\n    margin: 0;\n    padding: 0;\n    z-index: 99998;\n    box-shadow: 0 0 10px 0;\n    transition: all .3s ease-in-out; }\n\n.simple-notification-wrapper {\n  width: 400px !important; }\n"

/***/ }),

/***/ 761:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = __webpack_require__(3);
let AppComponent = class AppComponent {
};
AppComponent = __decorate([
    core_1.Component({
        selector: 'scatl',
        template: `
        <router-outlet></router-outlet>
    `,
    })
], AppComponent);
exports.AppComponent = AppComponent;


/***/ }),

/***/ 762:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const product_list_service_1 = __webpack_require__(153);
const query_data_service_1 = __webpack_require__(102);
const async_with_loading_bar_decorator_1 = __webpack_require__(312);
const ng2_slim_loading_bar_1 = __webpack_require__(101);
let ProductListComponent = class ProductListComponent {
    // noinspection JSUnusedGlobalSymbols
    constructor(loadingBarService, queryDataService, productListService) {
        this.loadingBarService = loadingBarService;
        this.queryDataService = queryDataService;
        this.productListService = productListService;
    }
    handlePaginationUpdate() {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.queryDataService.updateQueryData();
            yield this.productListService.updateList();
        });
    }
};
__decorate([
    async_with_loading_bar_decorator_1.asyncWithLoadingBar,
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], ProductListComponent.prototype, "handlePaginationUpdate", null);
ProductListComponent = __decorate([
    core_1.Component({
        selector: 'product-list',
        template: __webpack_require__(764),
        styles: [__webpack_require__(765)],
    }),
    __metadata("design:paramtypes", [ng2_slim_loading_bar_1.SlimLoadingBarService,
        query_data_service_1.QueryDataService,
        product_list_service_1.ProductListService])
], ProductListComponent);
exports.ProductListComponent = ProductListComponent;


/***/ }),

/***/ 763:
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
function deserializeProductList(response) {
    let productList = [];
    let productListRaw = response.json().results;
    for (let productRaw of productListRaw) {
        let product = {
            // TODO translation
            name: productRaw.translations.en.name,
            url: productRaw.url,
            price: productRaw.price,
            imageUrl: productRaw.primary_image_url,
        };
        productList.push(product);
    }
    return productList;
}
exports.deserializeProductList = deserializeProductList;


/***/ }),

/***/ 764:
/***/ (function(module, exports) {

module.exports = "<main id=\"product-list\"><div class=\"grid\"><div class=\"product-block\" *ngFor=\"let product of productListService.productList\"><div class=\"product\"><a href=\"{{ product.url }}\"><section class=\"product-image-block\"></section><section class=\"product-image-block\"><img class=\"product-image\" src=\"{{ product.imageUrl }}\"/></section><section class=\"product-details-block\"><span class=\"product-price\">$ {{ product.price | number }}</span><span class=\"product-name\">{{ product.name }}</span></section></a></div></div></div><pagination-form [queryData]=\"queryDataService.queryData\" (updatedEvent)=\"handlePaginationUpdate()\"></pagination-form></main>";

/***/ }),

/***/ 765:
/***/ (function(module, exports) {

module.exports = "#product-list {\n  display: flex;\n  flex-flow: column; }\n  #product-list .product-block {\n    position: relative;\n    padding-left: 15px;\n    padding-right: 15px; }\n    @media (min-width: 768px) {\n      #product-list .product-block {\n        float: left;\n        width: 50%; } }\n    @media (min-width: 992px) {\n      #product-list .product-block {\n        float: left;\n        width: 33.33333333%; }\n        #product-list .product-block:nth-child(3n+1) {\n          clear: both; } }\n    #product-list .product-block .product {\n      display: block;\n      position: relative;\n      width: 100%;\n      max-width: 280px;\n      margin-bottom: 30px;\n      padding: 10px 0;\n      border: 1px solid #ededed;\n      border-bottom: 2px solid #ddd;\n      background: #fff;\n      text-align: center; }\n      #product-list .product-block .product:hover {\n        box-shadow: 0 0 5px 0 rgba(0, 0, 0, 0.15); }\n        #product-list .product-block .product:hover .product-name {\n          color: #1bab95 !important; }\n      #product-list .product-block .product a:hover {\n        text-decoration: none; }\n      #product-list .product-block .product .product-image-block {\n        display: flex;\n        align-content: center;\n        align-items: center;\n        justify-content: center;\n        padding: 2px 15px; }\n        #product-list .product-block .product .product-image-block .product-image {\n          max-width: 100%;\n          max-height: 280px; }\n      #product-list .product-block .product .product-details-block {\n        display: flex;\n        flex-direction: column; }\n        #product-list .product-block .product .product-details-block .product-price {\n          margin: 12px 15px 0;\n          color: #1bab95;\n          font-weight: 700;\n          font-size: 16px; }\n        #product-list .product-block .product .product-details-block .product-name {\n          margin: 6px 15px;\n          color: #4c5969; }\n"

/***/ }),

/***/ 766:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const query_data_service_1 = __webpack_require__(102);
const product_list_service_1 = __webpack_require__(153);
const router_1 = __webpack_require__(93);
const async_with_loading_bar_decorator_1 = __webpack_require__(312);
const ng2_slim_loading_bar_1 = __webpack_require__(101);
const notify_service_1 = __webpack_require__(103);
const with_notify_decorator_1 = __webpack_require__(155);
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
            yield this.queryDataService.updateQueryData();
            yield this.productListService.updateList();
        });
    }
    handleQueryDataUpdate() {
        return __awaiter(this, void 0, void 0, function* () {
            this.resetPaginationForm();
            yield this.queryDataService.updateQueryData();
            yield this.productListService.updateList();
        });
    }
    loadQueryDataFromUrl() {
        this.queryDataService.initQueryDataFromPageUrl(this.activatedRoute.snapshot);
    }
    resetPaginationForm() {
        this.queryDataService.queryData.pageCurrent = 1;
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
        template: __webpack_require__(767),
        styles: [__webpack_require__(768)],
    }),
    __metadata("design:paramtypes", [ng2_slim_loading_bar_1.SlimLoadingBarService,
        notify_service_1.NotifyService,
        query_data_service_1.QueryDataService,
        router_1.ActivatedRoute,
        product_list_service_1.ProductListService])
], ControlFormComponent);
exports.ControlFormComponent = ControlFormComponent;


/***/ }),

/***/ 767:
/***/ (function(module, exports) {

module.exports = "<aside id=\"params-block\"><section id=\"params-form\"><sorting-form [queryData]=\"queryDataService.queryData\" (updatedEvent)=\"handleQueryDataUpdate()\"></sorting-form><price-range-form [queryData]=\"queryDataService.queryData\" (updatedEvent)=\"handleQueryDataUpdate()\"></price-range-form><attrim-form [queryData]=\"queryDataService.queryData\" (updatedEvent)=\"handleQueryDataUpdate()\"></attrim-form></section></aside>";

/***/ }),

/***/ 768:
/***/ (function(module, exports) {

module.exports = "#params-block {\n  margin-left: 15px;\n  margin-right: 15px; }\n"

/***/ }),

/***/ 769:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const core_2 = __webpack_require__(3);
const core_3 = __webpack_require__(3);
const core_4 = __webpack_require__(3);
const query_data_model_1 = __webpack_require__(20);
let AttrimFormComponent = class AttrimFormComponent {
    constructor() {
        this.updatedEvent = new core_4.EventEmitter();
    }
    // noinspection JSUnusedGlobalSymbols
    setQueryData(input) {
        let isClsFromInput = (cls) => cls.code === input.name;
        let clsFromInput = this.queryData.attrimClsArray.find(isClsFromInput);
        let isOptionFromInput = (clsOption) => {
            return clsOption.value === input.value;
        };
        let optionFromInput = clsFromInput.options.find(isOptionFromInput);
        optionFromInput.isSelected = input.checked;
        this.updatedEvent.emit();
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], AttrimFormComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], AttrimFormComponent.prototype, "updatedEvent", void 0);
AttrimFormComponent = __decorate([
    core_1.Component({
        selector: 'attrim-form',
        template: __webpack_require__(770),
        styles: [__webpack_require__(771)],
    })
], AttrimFormComponent);
exports.AttrimFormComponent = AttrimFormComponent;


/***/ }),

/***/ 770:
/***/ (function(module, exports) {

module.exports = "<section id=\"attrim-block\"><div class=\"class\" *ngFor=\"let cls of queryData.attrimClsArray\"><span class=\"class-name\">{{ cls.name }}</span><ul class=\"option-list\"><li class=\"option\" *ngFor=\"let option of cls.options\"><label class=\"option-label\"><input class=\"option-input\" type=\"checkbox\" [name]=\"cls.code\" [value]=\"option.value\" [checked]=\"option.isSelected\" (change)=\"setQueryData($event.target)\"/><span class=\"option-value\">{{ option.value }}</span></label></li></ul></div></section>";

/***/ }),

/***/ 771:
/***/ (function(module, exports) {

module.exports = "#attrim-block .class {\n  margin-bottom: 6px; }\n  #attrim-block .class:last-child {\n    border-bottom: 1px solid #d2d2d2; }\n  #attrim-block .class .class-name {\n    display: flex;\n    padding: 8px 13px;\n    margin: 0;\n    background-color: #6d7178;\n    color: #fff;\n    cursor: default; }\n  #attrim-block .class .option-list {\n    margin: 0;\n    padding: 13px 15px; }\n    #attrim-block .class .option-list .option {\n      margin: 1px 0;\n      list-style-type: none; }\n      #attrim-block .class .option-list .option .option-label {\n        display: flex;\n        margin: 0;\n        align-items: center; }\n        #attrim-block .class .option-list .option .option-label input {\n          margin-top: 0;\n          margin-right: 6px; }\n"

/***/ }),

/***/ 772:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const core_2 = __webpack_require__(3);
const core_3 = __webpack_require__(3);
const core_4 = __webpack_require__(3);
const query_data_model_1 = __webpack_require__(20);
const query_data_model_2 = __webpack_require__(20);
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
        template: __webpack_require__(773),
        styles: [__webpack_require__(774)],
    })
], SortingFormComponent);
exports.SortingFormComponent = SortingFormComponent;


/***/ }),

/***/ 773:
/***/ (function(module, exports) {

module.exports = "<section id=\"sorting-block\"><span id=\"heading\">Sorting</span><ul id=\"list\"><li><label><input name=\"sorting\" type=\"radio\" [value]=\"sorting.PriceMinMax\" [checked]=\"sorting.PriceMinMax === queryData.sorting\" (change)=\"setSorting($event.target)\"/><span>cheap first</span></label></li><li><label><input name=\"sorting\" type=\"radio\" [value]=\"sorting.PriceMaxMin\" [checked]=\"sorting.PriceMaxMin === queryData.sorting\" (change)=\"setSorting($event.target)\"/><span>expensive first</span></label></li><li><label><input name=\"sorting\" type=\"radio\" [value]=\"sorting.NameAZ\" [checked]=\"sorting.NameAZ === queryData.sorting\" (change)=\"setSorting($event.target)\"/><span>name A-Z</span></label></li><li><label><input name=\"sorting\" type=\"radio\" [value]=\"sorting.NameZA\" [checked]=\"sorting.NameZA === queryData.sorting\" (change)=\"setSorting($event.target)\"/><span>name Z-A</span></label></li></ul></section>";

/***/ }),

/***/ 774:
/***/ (function(module, exports) {

module.exports = "#sorting-block {\n  margin-bottom: 6px; }\n  #sorting-block #heading {\n    display: flex;\n    padding: 8px 13px;\n    margin: 0;\n    background-color: #6d7178;\n    color: #fff;\n    cursor: default; }\n  #sorting-block #list {\n    margin: 0;\n    padding: 13px 15px; }\n    #sorting-block #list li {\n      list-style-type: none; }\n      #sorting-block #list li label {\n        display: flex;\n        margin: 0;\n        align-items: center; }\n        #sorting-block #list li label input {\n          margin-top: 0;\n          margin-right: 5px; }\n"

/***/ }),

/***/ 775:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const core_2 = __webpack_require__(3);
const core_3 = __webpack_require__(3);
const core_4 = __webpack_require__(3);
const forms_1 = __webpack_require__(60);
const query_data_model_1 = __webpack_require__(20);
const core_5 = __webpack_require__(3);
let PriceRangeFormComponent = class PriceRangeFormComponent {
    constructor(formBuilder) {
        this.updatedEvent = new core_4.EventEmitter();
        this.config = {
            connect: true,
            step: 1,
            range: {
                min: window.DJANGO.priceRange.min,
                max: window.DJANGO.priceRange.max,
            },
            tooltips: [false, false],
        };
        this.formBuilder = formBuilder;
    }
    ngOnInit() {
        this.priceRange = [
            this.queryData.priceRange.min,
            this.queryData.priceRange.max,
        ];
        this.formGroup = this.formBuilder.group({
            slider: [this.priceRange],
            priceMin: [this.priceRange[0]],
            priceMax: [this.priceRange[1]],
        });
    }
    // noinspection JSUnusedGlobalSymbols
    updateFromMinInput(value) {
        this.queryData.priceRange.min = Number(value);
        this.syncPriceRangeForm();
        this.updatedEvent.emit();
    }
    // noinspection JSUnusedGlobalSymbols
    updateFromMaxInput(value) {
        this.queryData.priceRange.max = Number(value);
        this.syncPriceRangeForm();
        this.updatedEvent.emit();
    }
    // noinspection JSUnusedGlobalSymbols
    updateFromSlider() {
        this.queryData.priceRange.min = this.priceRange[0];
        this.queryData.priceRange.max = this.priceRange[1];
        this.syncPriceRangeForm();
        this.updatedEvent.emit();
    }
    /**
     * ngModel won't help, because of the angular bug with the input[type=number]
     */
    syncPriceRangeForm() {
        let formControls = this.formGroup.controls;
        let slider = formControls['slider'];
        slider.setValue([this.queryData.priceRange.min, this.queryData.priceRange.max]);
        let priceMin = formControls['priceMin'];
        priceMin.setValue(this.queryData.priceRange.min);
        let priceMax = formControls['priceMax'];
        priceMax.setValue(this.queryData.priceRange.max);
    }
};
__decorate([
    core_2.Input(),
    __metadata("design:type", query_data_model_1.QueryData)
], PriceRangeFormComponent.prototype, "queryData", void 0);
__decorate([
    core_3.Output(),
    __metadata("design:type", core_4.EventEmitter)
], PriceRangeFormComponent.prototype, "updatedEvent", void 0);
PriceRangeFormComponent = __decorate([
    core_1.Component({
        selector: 'price-range-form',
        template: __webpack_require__(776),
        styles: [__webpack_require__(777)],
        encapsulation: core_5.ViewEncapsulation.None,
    }),
    __metadata("design:paramtypes", [forms_1.FormBuilder])
], PriceRangeFormComponent);
exports.PriceRangeFormComponent = PriceRangeFormComponent;


/***/ }),

/***/ 776:
/***/ (function(module, exports) {

module.exports = "<form id=\"price-range-form\" [formGroup]=\"formGroup\"><p id=\"price-range-heading\">Price</p><div id=\"price-range-body\"><div id=\"price-range-block\"><input class=\"price-input\" type=\"number\" name=\"price-min\" [formControl]=\"formGroup.controls.priceMin\" [value]=\"priceRange[0]\" (change)=\"updateFromMinInput($event.target.value)\"/><span id=\"price-input-divider\">-</span><input class=\"price-input\" type=\"number\" name=\"price-max\" [formControl]=\"formGroup.controls.priceMax\" [value]=\"priceRange[1]\" (change)=\"updateFromMaxInput($event.target.value)\"/></div><nouislider [config]=\"config\" [formControl]=\"formGroup.controls.slider\" [(ngModel)]=\"priceRange\" (change)=\"updateFromSlider()\"></nouislider></div></form>";

/***/ }),

/***/ 777:
/***/ (function(module, exports) {

module.exports = "#price-range-form {\n  margin-bottom: 6px; }\n  #price-range-form #price-range-heading {\n    display: flex;\n    padding: 8px 13px;\n    margin: 0;\n    background-color: #6d7178;\n    color: #fff;\n    cursor: default; }\n  #price-range-form #price-range-body {\n    padding: 13px 15px; }\n    #price-range-form #price-range-body #price-range-block {\n      display: flex;\n      align-items: center; }\n      #price-range-form #price-range-body #price-range-block #price-input-divider {\n        margin: 0 3px; }\n      #price-range-form #price-range-body #price-range-block .price-input {\n        max-width: 75px;\n        padding: 4px 9px;\n        border: 1px solid #d7dde4;\n        box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);\n        transition: border-color ease-in-out .15s, box-shadow ease-in-out .15s; }\n        #price-range-form #price-range-body #price-range-block .price-input:focus {\n          box-shadow: none;\n          border-color: #1bab95;\n          outline: 0; }\n    #price-range-form #price-range-body nouislider {\n      margin: 10px auto;\n      width: 85%; }\n      #price-range-form #price-range-body nouislider .noUi-horizontal .noUi-handle {\n        width: 28px; }\n        #price-range-form #price-range-body nouislider .noUi-horizontal .noUi-handle:before {\n          left: 11px; }\n        #price-range-form #price-range-body nouislider .noUi-horizontal .noUi-handle:after {\n          left: 14px; }\n"

/***/ }),

/***/ 778:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const core_2 = __webpack_require__(3);
const core_3 = __webpack_require__(3);
const core_4 = __webpack_require__(3);
const query_data_model_1 = __webpack_require__(20);
const core_5 = __webpack_require__(3);
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
        template: __webpack_require__(779),
        styles: [__webpack_require__(780)],
        encapsulation: core_5.ViewEncapsulation.None,
    })
], PaginationFormComponent);
exports.PaginationFormComponent = PaginationFormComponent;


/***/ }),

/***/ 779:
/***/ (function(module, exports) {

module.exports = "<div id=\"pagination-form\"><button class=\"page-button page-boundary-button fa fa-angle-left\" id=\"previous\" (click)=\"setPage(queryData.pageCurrent - 1)\" [disabled]=\"queryData.pageCurrent === queryData.pageFirst\"></button><button class=\"page-button\" id=\"start\" (click)=\"setPage(queryData.pageFirst)\" [disabled]=\"queryData.pageCurrent === queryData.pageFirst\" [class.current-page]=\"isCurrentPage(queryData.pageFirst)\">{{ queryData.pageFirst }}</button><page-range [queryData]=\"queryData\" (updatedEvent)=\"updateQueryData()\"></page-range><button class=\"page-button\" id=\"end\" *ngIf=\"isEndButtonShouldBePresent()\" (click)=\"setPage(queryData.pageLast)\" [disabled]=\"queryData.pageCurrent === queryData.pageLast\" [class.current-page]=\"isCurrentPage(queryData.pageLast)\">{{ queryData.pageLast }}</button><button class=\"page-button page-boundary-button fa fa-angle-right\" id=\"next\" (click)=\"setPage(queryData.pageCurrent + 1)\" [disabled]=\"queryData.pageCurrent === queryData.pageLast\"></button></div>";

/***/ }),

/***/ 780:
/***/ (function(module, exports) {

module.exports = "#pagination-form {\n  display: flex;\n  margin: 7px 0;\n  justify-content: center; }\n  #pagination-form .page-button {\n    padding: 6px 12px;\n    margin-right: -1px;\n    border: 1px solid #D7DDE4;\n    color: #1BAB95;\n    background-color: #fff; }\n    #pagination-form .page-button.current-page {\n      color: #fff;\n      background-color: #1BAB95;\n      cursor: default; }\n      #pagination-form .page-button.current-page:hover {\n        color: #fff;\n        background-color: #1BAB95; }\n    #pagination-form .page-button:hover {\n      color: #11695b;\n      background-color: #fafbfb;\n      border-color: #D7DDE4; }\n    #pagination-form .page-button:focus {\n      outline: none; }\n  #pagination-form .page-boundary-button:hover {\n    color: #11695b;\n    background-color: #fafbfb;\n    border-color: #D7DDE4; }\n  #pagination-form .page-boundary-button:disabled {\n    color: #A4B1C2;\n    background-color: #fff;\n    border-color: #D7DDE4;\n    cursor: not-allowed; }\n    #pagination-form .page-boundary-button:disabled:hover {\n      background-color: #fff; }\n"

/***/ }),

/***/ 781:
/***/ (function(module, exports, __webpack_require__) {

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
const core_1 = __webpack_require__(3);
const core_2 = __webpack_require__(3);
const core_3 = __webpack_require__(3);
const core_4 = __webpack_require__(3);
const query_data_model_1 = __webpack_require__(20);
const page_range_service_1 = __webpack_require__(313);
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
        template: __webpack_require__(782),
    }),
    __metadata("design:paramtypes", [page_range_service_1.PageRangeService])
], PageRangeComponent);
exports.PageRangeComponent = PageRangeComponent;


/***/ }),

/***/ 782:
/***/ (function(module, exports) {

module.exports = "<span class=\"ellipsis left\" *ngIf=\"isLeftEllipsisRequired()\">...</span><button class=\"page-button\" *ngFor=\"let page of getPageArrayRange()\" (click)=\"setPage(page)\" [class.current-page]=\"isCurrentPage(page)\" [disabled]=\"isCurrentPage(page)\">{{ page }}</button><span class=\"ellipsis right\" *ngIf=\"isRightEllipsisRequired()\">...</span>";

/***/ })

},[757]);