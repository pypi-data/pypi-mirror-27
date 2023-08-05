"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@angular/core");
const forms_1 = require("@angular/forms");
const forms_2 = require("@angular/forms");
const forms_3 = require("@angular/forms");
const platform_browser_1 = require("@angular/platform-browser");
const http_1 = require("@angular/http");
const ng2_nouislider_1 = require("ng2-nouislider");
const app_routing_1 = require("app/app.routing");
const app_comp_1 = require("app/app.comp");
const product_list_comp_1 = require("app/product-list/product-list.comp");
const control_form_comp_1 = require("app/control-form/control-form.comp");
const query_data_network_service_1 = require("app/shared/query-data/query-data-network.service");
const product_list_service_1 = require("app/shared/product-list/product-list.service");
const catalog_comp_1 = require("app/catalog.comp");
const attrim_form_comp_1 = require("app/control-form/components/attrim-form.comp");
const sorting_form_comp_1 = require("app/control-form/components/sorting-form.comp");
const price_range_form_comp_1 = require("app/control-form/components/price-range-form.comp");
const pagination_form_comp_1 = require("app/product-list/pagination-form/pagination-form.comp");
const page_range_service_1 = require("app/product-list/pagination-form/page-range.service");
const route_params_1 = require("app/shared/query-data/serializers/route-params");
const route_snapshot_1 = require("app/shared/query-data/deserializers/route-snapshot");
const search_params_1 = require("app/shared/query-data/serializers/search-params");
const json_1 = require("app/shared/query-data/deserializers/json");
const page_range_comp_1 = require("app/product-list/pagination-form/page-range.comp");
const query_data_service_1 = require("app/shared/query-data/query-data.service");
const notify_service_1 = require("app/shared/notify.service");
const angular2_notifications_1 = require("angular2-notifications");
const ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
const animations_1 = require("@angular/platform-browser/animations");
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
//# sourceMappingURL=app.module.js.map