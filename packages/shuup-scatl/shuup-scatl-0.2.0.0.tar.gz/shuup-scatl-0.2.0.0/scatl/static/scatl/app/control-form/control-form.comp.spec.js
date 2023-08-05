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
const testing_1 = require("@angular/core/testing");
const control_form_comp_1 = require("app/control-form/control-form.comp");
const product_list_service_1 = require("app/shared/product-list/product-list.service");
const query_data_network_service_1 = require("app/shared/query-data/query-data-network.service");
const router_1 = require("@angular/router");
const router_2 = require("@angular/router");
const query_data_1 = require("testutils/generators/query-data");
const platform_browser_1 = require("@angular/platform-browser");
const query_data_model_1 = require("app/shared/query-data/query-data.model");
const platform_browser_2 = require("@angular/platform-browser");
const forms_1 = require("@angular/forms");
const forms_2 = require("@angular/forms");
const ng2_nouislider_1 = require("ng2-nouislider");
const attrim_form_comp_1 = require("app/control-form/components/attrim-form.comp");
const sorting_form_comp_1 = require("app/control-form/components/sorting-form.comp");
const price_range_form_comp_1 = require("app/control-form/components/price-range-form.comp");
const django_env_1 = require("testutils/mocks/django-env");
const route_snapshot_1 = require("app/shared/query-data/deserializers/route-snapshot");
const route_params_1 = require("app/shared/query-data/serializers/route-params");
const query_data_service_1 = require("app/shared/query-data/query-data.service");
const ng2_slim_loading_bar_1 = require("ng2-slim-loading-bar");
const notify_service_1 = require("app/shared/notify.service");
const angular2_notifications_1 = require("angular2-notifications");
describe('control-form', () => {
    let self;
    beforeEach((done) => __awaiter(this, void 0, void 0, function* () {
        django_env_1.initDjangoEnv();
        yield initAngularEnv();
        initTestSuite();
        done();
    }));
    function initAngularEnv() {
        return __awaiter(this, void 0, void 0, function* () {
            // noinspection JSUnusedGlobalSymbols
            yield testing_1.TestBed.configureTestingModule({
                imports: [
                    platform_browser_2.BrowserModule,
                    forms_1.FormsModule,
                    forms_2.ReactiveFormsModule,
                    ng2_nouislider_1.NouisliderModule,
                    angular2_notifications_1.SimpleNotificationsModule.forRoot(),
                ],
                declarations: [
                    control_form_comp_1.ControlFormComponent,
                    sorting_form_comp_1.SortingFormComponent,
                    attrim_form_comp_1.AttrimFormComponent,
                    price_range_form_comp_1.PriceRangeFormComponent,
                ],
                providers: [
                    { provide: route_snapshot_1.RouteSnapshotToQueryDataDeserializer, useValue: {}, },
                    { provide: route_params_1.QueryDataToRouteParamsSerializer, useValue: {}, },
                    { provide: router_2.Router, useValue: {}, },
                    { provide: product_list_service_1.ProductListService, useValue: {}, },
                    { provide: query_data_network_service_1.QueryDataNetworkService, useValue: {}, },
                    { provide: router_1.ActivatedRoute, useValue: {}, },
                    notify_service_1.NotifyService,
                    query_data_service_1.QueryDataService,
                    ng2_slim_loading_bar_1.SlimLoadingBarService,
                ],
            })
                .compileComponents();
        });
    }
    function initTestSuite() {
        let fixture = testing_1.TestBed.createComponent(control_form_comp_1.ControlFormComponent);
        let gen = new query_data_1.QueryDataGenerator();
        self = {
            compFixture: fixture,
            compDebug: fixture.debugElement,
            comp: fixture.componentInstance,
            dataSource: gen.data(),
            queryDataService: testing_1.TestBed.get(query_data_service_1.QueryDataService),
        };
        // `callFake` because `callThrough` doesn't work
        // (jasmine core 2.7.0, angular 5.0.1)
        spyOn(self.comp, 'ngOnInit').and.callFake(() => { });
        spyOn(self.comp, 'handleQueryDataUpdate').and.callFake(() => { });
        self.queryDataService.queryData = self.dataSource;
        self.compFixture.detectChanges();
    }
    it('renders expected values', () => {
        let sortingCheckedSelector = platform_browser_1.By.css(`input[name='sorting']:checked`);
        let sortingChecked = self.compDebug.query(sortingCheckedSelector);
        expect(sortingChecked.properties['value']).toBe(self.dataSource.sorting);
        for (let clsSource of self.dataSource.attrimClsArray) {
            let optionSelector = platform_browser_1.By.css(`input[name='${clsSource.code}']`);
            let optionsRendered = self.compDebug.queryAll(optionSelector);
            for (let optionRendered of optionsRendered) {
                let isOptionSource = (option) => {
                    return option.value === optionRendered.properties['value'];
                };
                let optionSource = clsSource.options.find(isOptionSource);
                expect(optionRendered.properties['checked']).toBe(optionSource.isSelected);
            }
        }
    });
    for (let arg of [
        { sortingOld: query_data_model_1.Sorting.NameAZ, sortingNew: query_data_model_1.Sorting.PriceMaxMin },
        { sortingOld: query_data_model_1.Sorting.NameZA, sortingNew: query_data_model_1.Sorting.PriceMaxMin },
        { sortingOld: query_data_model_1.Sorting.PriceMaxMin, sortingNew: query_data_model_1.Sorting.PriceMinMax },
    ]) {
        it(`updates the sorting (from ${arg.sortingOld} to ${arg.sortingNew})`, (done) => __awaiter(this, void 0, void 0, function* () {
            setComponentSorting(arg.sortingOld);
            expect(self.queryDataService.queryData.sorting).toBe(arg.sortingOld);
            yield selectSorting(arg.sortingNew);
            expect(self.queryDataService.queryData.sorting).toBe(arg.sortingNew);
            done();
        }));
    }
    it('inits the price range', () => {
        expect(self.queryDataService.queryData.priceRange.min).toBe(self.dataSource.priceRange.min);
        expect(self.queryDataService.queryData.priceRange.max).toBe(self.dataSource.priceRange.max);
    });
    function setComponentSorting(sortingNew) {
        self.queryDataService.queryData.sorting = sortingNew;
        self.compFixture.detectChanges();
    }
    function selectSorting(sorting) {
        return __awaiter(this, void 0, void 0, function* () {
            let sortingNewSelector = platform_browser_1.By.css(`input[name='sorting'][value='${sorting}']`);
            let sortingNewDebug = self.compDebug.query(sortingNewSelector);
            let sortingNewElem = sortingNewDebug.nativeElement;
            sortingNewElem.click();
            yield self.compFixture.whenStable();
        });
    }
});
//# sourceMappingURL=control-form.comp.spec.js.map