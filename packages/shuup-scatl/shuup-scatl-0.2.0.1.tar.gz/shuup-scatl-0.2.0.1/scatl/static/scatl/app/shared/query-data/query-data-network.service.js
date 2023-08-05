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
const search_params_1 = require("app/shared/query-data/serializers/search-params");
const json_1 = require("app/shared/query-data/deserializers/json");
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
//# sourceMappingURL=query-data-network.service.js.map